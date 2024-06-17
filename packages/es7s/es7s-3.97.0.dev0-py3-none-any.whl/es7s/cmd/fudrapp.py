# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import base64
import dataclasses
import io
import json
import os
import re
import sys
import tempfile
import time
import typing as t
from collections import deque, Counter
from collections.abc import Sequence
from dataclasses import dataclass, field
from functools import cached_property, cache
from math import floor, ceil, log
from threading import Lock
from uuid import UUID

import pytermor as pt
from PIL import Image, ImageFont
from PIL.ImageDraw import Draw

from es7s.cli._base_opts_params import OPT_VALUE_AUTO
from es7s.cmd._base import _BaseAction
from es7s.cmd._adaptive_input import _AdaptiveInputAction
from es7s.cmd._multi_threaded import _MultiThreadedAction
from es7s.shared import (
    get_logger,
    get_stdout,
    SMALLEST_PIXEL_7,
    ShutdownableThread,
    with_terminal_state,
    ProxiedTerminalState,
    ShutdownInProgress,
    boolsplit,
    sub,
    get_stderr,
    is_x11,
    run_subprocess,
    find_executable,
)
from es7s.shared.fusion_brain import FusionBrainAPI
from es7s.shared.path import get_font_file
from es7s.shared.pt_ import (
    ElasticFragment,
    ElasticSetup as ES,
    ElasticContainer,
    ElasticSetup,
)
from es7s.shared.uconfig import get_merged, get_for


@dataclass(frozen=True)
class Prompt:
    prompt_idx: int
    input_line_idx: int
    input_line: str
    style: str

    @cached_property
    def is_default(self) -> bool:
        return self.style == "DEFAULT"

    @cache
    def asdict(self) -> dict:
        return dataclasses.asdict(self)


@dataclass
class MergeImageTask:
    prompt: Prompt
    output_filename: str
    input_filepath: str


class action(_MultiThreadedAction, _AdaptiveInputAction, _BaseAction):
    def __init__(self, style: str, all_styles: bool, **kwargs):
        super().__init__(**kwargs)
        del kwargs["threads"]

        auth_cfg = get_merged().get_section("auth")
        self._api = FusionBrainAPI(
            auth_cfg.get("fusion-brain-api-key"),
            auth_cfg.get("fusion-brain-secret"),
        )
        if not self._auth():
            return

        api_styles = self._api.fetch_styles()
        api_styles_msg = "Supported styles: " + ", ".join(api_styles)
        get_logger().info(api_styles_msg)
        if style not in api_styles:
            get_logger().warning(f"Invalid style '{style}'. {api_styles_msg}")

        self._prompts = deque[Prompt]()
        styles = ([style], api_styles)[all_styles]
        for (idx, ln) in enumerate(self._input_lines):
            for style in styles:
                self._prompts.append(Prompt(len(self._prompts), idx, ln, style))

        self._queue = Queue(self._api, self._threads, self._prompts, **kwargs)
        self._run(**kwargs)

    def _auth(self) -> bool:
        try:
            return bool(self._api.fetch_model())
        except Exception as e:
            raise RuntimeError("Auth failed, unable to proceed") from e

    @with_terminal_state(no_cursor=True)
    def _run(self, termstate: ProxiedTerminalState, **kwargs):
        try:
            sys.stdout.flush()
            self._queue.run()
        finally:
            merge_tasks = self._queue.results
            self._queue.destroy()
            self._merge_results(merge_tasks, **kwargs)

    def _merge_results(
        self,
        merge_tasks: list[MergeImageTask],
        width: int,
        no_open: bool,
        delete: bool,
        **_,
    ):
        im = ImageMerger(self._input_lines, width)
        merged_paths = im.merge_all(merge_tasks, not delete)
        open_merged = not no_open

        if merged_paths:
            for merged_path in merged_paths:
                get_stdout().echo(merged_path)
            if is_x11() and open_merged:
                run_subprocess("xdg-open", merged_paths[0])


class Queue:
    _THREAD_POLL_TIME_SEC = 0.1

    start_ts: float = None

    @staticmethod
    def now() -> float:
        return time.time_ns()

    def __init__(
        self,
        api: FusionBrainAPI,
        threads: int,
        prompts: Sequence[Prompt],
        width: int,
        height: int,
        times: int,
        retries: int,
        no_retry: bool,
        **_,
    ):
        self.tasks = deque[GenerationTask]()
        self.tasks_done = deque[GenerationTask]()
        self.tasks_lock = Lock()

        self._workers = deque[Worker](maxlen=threads)
        self._exceptions = deque[tuple["Worker", t.Optional["Task"], Exception]]()
        self.results: list["MergeImageTask"] = []

        super().__init__()

        tasks_total = times * len(prompts)
        for _ in range(times):
            for p in prompts:
                task_idx = len(self.tasks)
                pre_start_delay_s = task_idx / 2 if task_idx < threads else 0
                task = GenerationTask(p, task_idx, tasks_total, pre_start_delay_s, (width, height))
                self.tasks.append(task)

        if retries == OPT_VALUE_AUTO:
            retries = max(0, 5 - ceil(log(tasks_total, 2)))
        if no_retry:
            retries = 0
            get_logger().info(f"Retries are disabled")
        else:
            get_logger().info(f"Retry amount is set to: {retries}")

        for w_idx in range(min(len(self.tasks), threads)):
            self._workers.append(Worker(w_idx, retries, self, api.copy()))

        self.pp = ProgressPrinter()

    def run(self):
        Queue.start_ts = Queue.now()

        for worker in self._workers:
            worker.start()

        while self._workers:
            worker: Worker = self._workers[0]
            worker.join(self._THREAD_POLL_TIME_SEC)

            if worker.is_alive():
                # self.pp.update(worker.task)  # avoid complete freezing on network delays
                self._workers.rotate()
            else:
                self._workers.remove(worker)

    def get_next_task(self) -> t.Optional["GenerationTask"]:
        if not self.tasks:
            return None
        if self.tasks_lock.acquire(timeout=1):
            task = self.tasks.popleft()
            task.task_start_ts = self.now() + task.pre_start_delay_s * 1e9
            self.tasks_lock.release()
            return task
        return None

    def set_task_completed(self, task: "GenerationTask"):
        task.is_finished = True
        self.tasks_done.append(task)

    def defer_exception(self, worker: "Worker", task: t.Optional["GenerationTask"], e: Exception):
        self._exceptions.append((worker, task, e))

    def defer_merge_image(self, merge_task: "MergeImageTask"):
        self.results.append(merge_task)

    def destroy(self):
        self.pp.close()
        self.pp.print_exceptions(self._exceptions)

        results = []
        for task in self.tasks_done:
            results.extend(task.statuses)

        results_by_type = Counter(results)

        job_durations: list[float] = []
        for task in self.tasks_done:
            if task.jobs_done:
                job_durations.extend(task.job_durations_ns)

        job_duration_stats = JobDurationStats()
        if job_durations:
            job_duration_stats = JobDurationStats(
                min(job_durations),
                sum(job_durations) / len(job_durations),
                max(job_durations),
            )
        self.pp.print_summary(results_by_type, job_duration_stats)


@dataclass
class JobDurationStats:
    min: float = None
    avg: float = None
    max: float = None


class Status(str, pt.ExtendedEnum):
    QUEUED = "queued"

    PENDING = "pending"
    REFUSED = "refused"
    RECEIVED = "received"
    ERROR = "error"

    CANCEL = "cancel"
    FAILURE = "failure"
    SUCCESS = "success"


@dataclass(frozen=True)
class StatusStyle:
    char: pt.RT
    name: pt.FT
    duration: pt.FT
    adjective: str = None

    @cached_property
    def msg(self) -> pt.FT:
        if self.name:
            return pt.FrozenStyle(self.name, bold=True)
        return pt.NOOP_STYLE


class StatusStyles(dict):
    def __init__(self):
        C_IP = "□"
        C_DONE = "■"
        ST_OK = pt.make_style(pt.cv.GREEN)
        ST_NOK = pt.make_style(pt.cv.RED)
        ST_WARN = pt.make_style(pt.cv.YELLOW)
        ST_STALE = pt.make_style(pt.cv.GRAY_50)
        ST_TIME = pt.make_style(pt.cv.BLUE)

        super().__init__(
            {
                Status.PENDING: self._make(C_IP, st_time=ST_TIME),
                Status.QUEUED: self._make(st_status=ST_STALE),
                Status.REFUSED: self._make(C_DONE, ST_WARN),
                Status.RECEIVED: self._make(C_IP, ST_OK),
                Status.ERROR: self._make(C_IP, ST_NOK),
                Status.CANCEL: self._make(C_IP, ST_NOK, adjective="cancelled"),
                Status.FAILURE: self._make(C_DONE, ST_NOK, adjective="failed"),
                Status.SUCCESS: self._make(C_DONE, ST_OK, adjective="successful"),
            }
        )

    @classmethod
    def _make(
        cls,
        char="",
        st_status: pt.FT = pt.NOOP_STYLE,
        st_time: pt.FT = pt.NOOP_STYLE,
        adjective: str = None,
    ) -> StatusStyle:
        """
        :param char:       icon to display
        :param st_status:  style to apply to status name AND char itself if
                           provided, otherwise NOOP
        :param st_time:    style to apply to duration if provided, otherwise ``st_status``
        """
        return StatusStyle(
            char=pt.Fragment(char, st_status) if st_status else char,
            name=st_status,
            duration=st_time or st_status,
            adjective=adjective,
        )


_styles = StatusStyles()


@dataclass(frozen=True)
class ReceivedImageInfo:
    path: str

    @cached_property
    def basename(self) -> str:
        return os.path.basename(self.path)

    @cached_property
    def size(self) -> int:
        return os.stat(self.path).st_size


@dataclass()
class GenerationTask:
    MIN_FETCH_INTERVAL_SEC = 4

    prompt: Prompt
    task_idx: int
    tasks_total: int
    pre_start_delay_s: float = 0.0
    size: tuple[int, int] = (1024, 1024)

    max_width: int = pt.get_terminal_width()

    job_uuid: UUID | None = None
    images_b64: list[str] = field(default_factory=list)
    statuses: list[Status] = field(default_factory=list)
    task_retries: int | None = None  # actually "tries"
    task_start_ts: float | None = None
    job_start_ts: float | None = None
    last_fetch_ts: float | None = None
    task_duration_ns: float | None = None
    job_durations_ns: list[float] = field(default_factory=list)
    jobs_done: int = 0
    msg: str | ReceivedImageInfo | None = None
    is_finished: bool = False

    @cached_property
    def state_printer(self) -> "TaskStatePrinter":
        return TaskStatePrinter(self)

    @property
    def current_status(self) -> Status:
        if not self.statuses:
            return Status.QUEUED
        return self.statuses[-1]

    def assign_job_uuid(self, uuid: UUID):
        self.job_uuid = uuid
        self.job_start_ts = Queue.now()
        self.last_fetch_ts = None

    def is_allowed_to_generate(self) -> bool:
        return Queue.now() >= self.task_start_ts

    def is_allowed_to_fetch(self) -> bool:
        if self.last_fetch_ts is None:
            return True
        return (Queue.now() - self.last_fetch_ts) / 1e9 >= self.MIN_FETCH_INTERVAL_SEC

    def set_status(self, rr: Status, msg: str | ReceivedImageInfo = None):
        self.statuses.append(rr)
        self.msg = msg
        self.last_fetch_ts = Queue.now()
        self.task_duration_ns = Queue.now() - self.task_start_ts

    def append_images(self, images_b64: list[str]):
        self.images_b64 += images_b64
        self.set_status(Status.RECEIVED)
        self.job_durations_ns.append(Queue.now() - self.job_start_ts)
        self.job_start_ts = None
        self.jobs_done += 1


class Worker(ShutdownableThread):
    _POLL_TIME_SEC = 0.15

    def __init__(
        self,
        worker_idx: int,
        retries: int,
        queue: Queue,
        api: FusionBrainAPI,
    ):
        self.worker_idx = worker_idx
        self._retries = retries
        self._queue = queue
        self._api = api

        self.task: GenerationTask | None = None

        super().__init__("fudra", thread_name=f"worker:{self.worker_idx}")

    def _reset(self):
        self.task = None

    def run(self):
        while True:
            if self.is_shutting_down():
                self.destroy()
                return

            if not self.task:
                self.task = self._queue.get_next_task()
                if not self.task:
                    self.shutdown()
                    continue

            if self.task:
                try:
                    self._generate()
                    self._write_image()
                except ShutdownInProgress:
                    pass
                except Exception as e:
                    self._queue.defer_exception(self, self.task, e)
                    self.task.set_status(Status.FAILURE, repr(e))
                finally:
                    self._queue.set_task_completed(self.task)
                    self._redraw()
                    self._reset()

    def _update(self):
        self._queue.pp.update(self.task)

    def _redraw(self):
        self._queue.pp.redraw(self.task)

    def _tick(self):
        if self.is_shutting_down():
            self.task.set_status(Status.CANCEL)
            raise ShutdownInProgress
        time.sleep(self._POLL_TIME_SEC)
        self._update()

    def _generate(self):
        gen_attempts = self._retries + 1
        self.task.task_retries = 0
        while gen_attempts > 0 and len(self.task.images_b64) == 0:
            if not self.task.is_allowed_to_generate():
                self._tick()
                continue

            gen_attempts -= 1
            negprompt, posprompt = boolsplit(
                self.task.prompt.input_line.split(), lambda p: bool(re.match(r"^-[^-]", p))
            )
            generation_uuid = self._api.generate(
                " ".join(posprompt),
                [np.removeprefix("-") for np in negprompt],
                self.task.prompt.style,
                self.task.size,
            )
            self.task.assign_job_uuid(generation_uuid)
            self.task.task_retries += 1
            self._update()

            fetch_attempts = 30
            while fetch_attempts > 0:
                self._tick()

                if self.task.is_allowed_to_fetch():
                    fetch_attempts -= 1
                    images_b64, censored, resp = self._api.check_generation(self.task.job_uuid)

                    if not resp.ok:
                        self.task.set_status(Status.ERROR, f"HTTP {resp.status_code}")
                        e = RuntimeError(f"Request failed with HTTP {resp.status_code}")
                        self._queue.defer_exception(self, self.task, e)
                    elif censored:
                        self.task.set_status(Status.REFUSED)
                    elif len(images_b64) > 0:
                        self.task.append_images(images_b64)
                    else:
                        self.task.set_status(Status.PENDING)

                    self._update()
                    if self.task.current_status != Status.PENDING:
                        break

            self._update()

    def _write_image(self):
        if not self.task.images_b64:
            return

        output_dir = os.path.expanduser(get_for(self).get("output-dir", str, fallback="~"))
        os.makedirs(output_dir, exist_ok=True)

        basename = f"fb-{Queue.start_ts / 1e9:.0f}"
        origin_basename = f"{basename}-{self.task.prompt.input_line_idx}-{self.task.task_idx}"
        merged_basename = f"{basename}-{self.task.prompt.input_line_idx}-merged"

        with open(os.path.join(output_dir, f"{origin_basename}.json"), "wt") as f:
            json.dump(self.task.prompt.asdict(), f)

        for idx, image_b64 in enumerate(self.task.images_b64):
            io_b64 = io.BytesIO(image_b64.encode("utf8"))
            io_raw = io.BytesIO()
            base64.decode(io_b64, io_raw)
            del io_b64

            fmt = "jpg"
            target_path = os.path.join(output_dir, f"{origin_basename}-{idx}.{fmt}")
            with open(target_path, "wb") as f:
                io_raw.seek(0)
                f.write(io_raw.read())
                del io_raw

            img_info = ReceivedImageInfo(target_path)
            self.task.set_status(Status.SUCCESS, img_info)
            self._queue.defer_merge_image(
                MergeImageTask(self.task.prompt, f"{merged_basename}.{fmt}", target_path)
            )


class ImageMerger:
    def __init__(self, input_lines: list[str], img_width: int):
        self._input_lines = input_lines
        self._img_width = img_width

        # keys are input line indexes
        self._input_path_map: dict[int, list[str]] = {}  # {0: [ipath0, ...], 1: [ipathN, ...], ...}
        self._output_name_map: dict[int, str] = {}  # {0: oname0, ...}

        self._labeler = ImageLabeler()

    def merge_all(
        self,
        merge_tasks: list[MergeImageTask],
        keep_origins: bool,
    ) -> list[str]:
        for merge_task in merge_tasks:
            self._add_image(merge_task)

        if not len(self._input_path_map.items()):
            return []

        if gmic := find_executable("gmic"):
            return self._merge_all_gmic(gmic, keep_origins)
        raise NotImplementedError("PIL fallback @TODO")

    def _add_image(self, merge_task: MergeImageTask):
        prompt = merge_task.prompt
        il_idx = prompt.input_line_idx
        if il_idx not in self._input_path_map.keys():
            self._input_path_map.update({il_idx: []})
        self._input_path_map.get(il_idx).append(merge_task.input_filepath)
        self._output_name_map.update({il_idx: merge_task.output_filename})

    def _merge_all_gmic(self, gmic_path: str, keep_origins: bool) -> list[str]:
        output_paths = []
        for input_line_idx, input_paths in self._input_path_map.items():
            input_line = self._input_lines[input_line_idx]
            out_filename = os.path.abspath(self._output_name_map[input_line_idx])
            label_filepath = self._labeler.make_label_image(input_line, self._img_width)
            args = [
                *input_paths,
                ("fx_montage", "5,,0,0,0,0,0,0,0,255,0,0,0,0,0"),
                label_filepath,
                ("append", "y"),
                ("normalize", "1,255"),
                ("o", out_filename),
            ]
            sub.run_subprocess(gmic_path, *pt.flatten(args), executable=gmic_path)
            os.unlink(label_filepath)

            output_paths.append(os.path.abspath(out_filename))
            if not keep_origins:
                get_logger().info("Removing the origins")
                for img in input_paths:
                    os.unlink(img)
            else:
                get_logger().info("Keeping the origins")
        return output_paths


class ImageLabeler:
    LABEL_FONT = ImageFont.truetype(str(get_font_file(SMALLEST_PIXEL_7)), 10)

    def make_label_image(self, input_line: str, width: int) -> str:
        input_line_split = []

        im = Image.new("RGBA", (width, 256))
        while input_line:
            tlen = Draw(im).textlength(input_line, self.LABEL_FONT)
            overflow_ratio = tlen / im.width
            edge = len(input_line) / overflow_ratio
            if overflow_ratio < 1:
                input_line_split.append(input_line)
                input_line = ""
            else:
                edge = floor(edge)
                try:
                    nearest_space = input_line.rindex(" ", 0, edge)
                    input_line_split.append(input_line[:nearest_space])
                    input_line = input_line[nearest_space + 1 :]
                except ValueError:
                    input_line_split.append(input_line[:edge])
                    input_line = input_line[edge:]

        input_line_joined = "\n".join(input_line_split)
        kwargs = dict(
            xy=(6, 6),
            text=input_line_joined,
            font=self.LABEL_FONT,
            stroke_width=1,
            spacing=0,
        )
        box = Draw(im).multiline_textbbox(**kwargs)
        imtx = Image.new("RGBA", box[2:], (255, 255, 255, 0))
        Draw(imtx).multiline_text(
            **kwargs,
            fill=(255, 255, 255, 255),
            stroke_fill=(0, 0, 0, 255),
        )
        im.paste(imtx, None, imtx)
        imtx.close()
        im = im.crop((0, 0, box[2] + box[0], box[3] + box[1]))

        fid, fpath = tempfile.mkstemp(suffix=".png")
        with open(fpath, "wb") as f:
            im.save(f)
            im.close()
        return fpath


# noinspection PyMethodMayBeStatic
class ProgressPrinter:
    _ts_last_termw_query: float = None
    _max_width: int = None

    def __init__(self):
        self._redraw_lock = Lock()
        self._cursor_line = 0
        self._task_lines: deque[GenerationTask | None] = deque()

    def update(self, task: GenerationTask):
        if not task:
            return
        with self._redraw_lock:
            if task not in self._task_lines:
                self._go_to_bottom()
                self._task_lines.append(task)
            else:
                task_line = self._task_lines.index(task)
                self._go_to(task_line)
            self._draw(task)

    def redraw(self, task: GenerationTask):
        self.update(task)
        with self._redraw_lock:
            self._task_lines[self._task_lines.index(task)] = None

    def _draw(self, task: GenerationTask, suffix: str = ""):
        get_stderr().echoi_rendered("\n")
        get_stderr().echoi_rendered(task.state_printer.print_state() + suffix)
        get_stderr().echoi(pt.make_move_cursor_up())

    def _go_to(self, target_line: int):
        delta = abs(self._cursor_line - target_line)
        if self._cursor_line > target_line:
            get_stderr().echoi(pt.make_move_cursor_up(delta))
        elif self._cursor_line < target_line:
            get_stderr().echoi(pt.make_move_cursor_down(delta))
        get_stderr().echoi(pt.make_set_cursor_column())
        self._cursor_line = target_line

    def _go_to_bottom(self):
        self._go_to(len(self._task_lines))

    def _clear_line(self):
        get_stderr().echoi(pt.make_clear_line())

    def close(self):
        self._go_to_bottom()
        get_stderr().echo("")

    def print_exceptions(
        self, exceptions: t.Sequence[tuple[Worker, GenerationTask | None, Exception]]
    ):
        if not exceptions:
            return
        get_stderr().echo(f"There was {len(exceptions)} error(s):")

        for (_, task, e) in exceptions:
            msg = pt.Text()
            if task:
                msg += pt.Fragment(pt.pad(2) + f"Task #{task.task_idx+1}", pt.Styles.ERROR_LABEL)
            msg += pt.Fragment(pt.pad(2) + repr(e), pt.Styles.ERROR)
            get_stderr().echo_rendered(msg)

    def print_summary(self, results_by_type: Counter[Status], job_duration_stats: JobDurationStats):
        def _print_sep():
            get_stderr().echo("\n" + ("-" * 40))

        def _print_summary_line(*f):
            get_stderr().echo_rendered(pt.Text(*f))

        def _count_status(*ss: Status) -> tuple[Status, int, pt.Style, str]:
            count = 0
            for s in ss:
                count += results_by_type.get(s) or 0

            output_status = ss[-1]
            status_st: StatusStyle = _styles.get(output_status)
            output_st = pt.FrozenStyle(fg=pt.cv.GRAY_50)
            if count > 0:
                output_st = status_st.name
            return output_status, count, output_st, status_st.adjective or output_status.value

        status_datas = [
            _count_status(Status.SUCCESS),
            _count_status(Status.REFUSED),
            _count_status(Status.CANCEL),
            _count_status(Status.ERROR, Status.FAILURE),
        ]
        requested = sum([s[1] for s in status_datas])

        stat_props = ["min", "avg", "max"]
        stat_values = [getattr(job_duration_stats, stat_prop) for stat_prop in stat_props]
        stat_frags = []
        for stat_value in stat_values:
            if stat_frags:
                stat_frags.append("/")
            if stat_value:
                stat_frags.append((pt.format_time_delta(stat_value / 1e9), pt.cv.BLUE))
            else:
                stat_frags.append(("---", pt.cv.GRAY_50))

        _print_sep()
        _print_summary_line(
            f"Total ",
            pt.Fragment(str(requested), pt.FrozenStyle(bold=True)),
            " requests in ",
            pt.format_time_delta((Queue.now() - Queue.start_ts) / 1e9),
            pt.cv.BLUE,
            ", including:",
        )
        for stdata in status_datas:
            status, status_count, st, val = stdata
            if status_count == 0:
                continue
            if status != Status.SUCCESS:
                status_ratio = (100 * status_count / requested) if requested else 0
                extra_info = (" (", f"{status_ratio:3.1f}%", st, ")")
            else:
                extra_info = (" (", *stat_frags, f" {'/'.join(stat_props)})")

            _print_summary_line(
                f" • {pt.Fragment(str(status_count), pt.FrozenStyle(st, bold=True))} {val}",
                *extra_info,
            )
        _print_sep()

    @classmethod
    def get_max_width(cls) -> int:
        if not cls._max_width or (time.time() - cls._ts_last_termw_query >= 1):
            cls._max_width = pt.get_terminal_width(pad=0)
            cls._ts_last_termw_query = time.time()
        return cls._max_width


class TaskStatePrinter:
    def __init__(self, task: GenerationTask):
        self._task = task

    def print_state(self) -> pt.RT:
        task = self._task

        stc: StatusStyle = _styles.get(task.current_status)
        st0 = pt.NOOP_STYLE

        def stmo(c: pt.Style):
            return st0.clone().merge_overwrite(c)

        def stmf(c: pt.Style):
            return st0.clone().merge_fallback(c)

        if task.is_finished:
            st0 = stmo(pt.Style(fg=pt.cv.GRAY_50))

        ec = ElasticContainer(
            ElasticFragment(f"{task.task_idx + 1}/{task.tasks_total} ", st0, es=ES(3, 7, ">")),
            self._print_prompt(task.prompt, st0, es=ES(6, 1.00)),
            self._print_msg(task, stmo(stc.msg), es=ES(6, 36)),
            ElasticFragment(task.current_status.value, stmo(stc.name), es=ES(4, 9, ">")),
            self._print_task_retries(task.task_retries, stmo(stc.name), es=ES(3, 4)),
            self._print_status_history(task.statuses, st0, 12),
            self._print_task_duration(task, stmf(stc.duration), es=ES(5, 8, ">")),
            width=ProgressPrinter.get_max_width(),
            gap=1,
        )

        return ec

    @classmethod
    def _print_prompt(cls, prompt: Prompt, st: pt.Style, es: ElasticSetup) -> ElasticFragment:
        msg_prompt = prompt.input_line
        if not prompt.is_default:
            msg_prompt = f"[{pt.cut(prompt.style, 7)}] {prompt.input_line}"
        return ElasticFragment(msg_prompt, st, es=es)

    @classmethod
    def _print_msg(cls, task: GenerationTask, st: pt.Style, es: ElasticSetup) -> ElasticFragment:
        if not task.msg:
            msg = str(task.job_uuid or "")
        else:
            gap = 1
            if isinstance(task.msg, ReceivedImageInfo):
                size_str = pt.format_bytes_human(task.msg.size).rjust(5)
                msg = (
                    pt.fit(task.msg.basename, es.max_width - len(size_str) - gap, "<")
                    + pt.pad(gap)
                    + size_str
                )
            else:
                msg = pt.fit(task.msg, es.max_width, "<", keep="<")

        return ElasticFragment(msg, st, es=es)

    @classmethod
    def _print_task_duration(
        cls, task: GenerationTask, st: pt.Style, es: ElasticSetup
    ) -> ElasticFragment:
        col_dur = "---"
        if task.task_start_ts and task.current_status != Status.QUEUED:
            task_start_delta = Queue.now() - task.task_start_ts
            if task_start_delta > 0:
                col_dur = pt.format_time_delta(task_start_delta / 1e9)

        return ElasticFragment(col_dur, st, es=es)

    @classmethod
    def _print_task_retries(
        cls, task_retries: int, st: pt.Style, es: ElasticSetup
    ) -> ElasticFragment:
        retries_str = ""
        if task_retries > 1:
            retries_str = f"({task_retries})"
        return ElasticFragment(retries_str, st, es=es)

    @classmethod
    def _print_status_history(cls, statuses: list[Status], defst: pt.Style, limit: int) -> pt.Text:
        def __iter():
            L = limit
            for status in reversed(statuses):
                if L <= 1:
                    yield pt.OVERFLOW_CHAR
                    break
                L -= 1
                char = _styles.get(status).char
                if isinstance(char, str):
                    yield pt.Fragment(char, defst)
                else:
                    yield char

        return pt.Text(*reversed([*__iter()]), width=limit)
