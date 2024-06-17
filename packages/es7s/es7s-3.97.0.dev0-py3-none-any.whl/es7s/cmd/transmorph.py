# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import random
import re
import typing as t
from collections import deque
from collections.abc import Iterable
from copy import copy
from dataclasses import dataclass
from threading import BoundedSemaphore, Event
from time import sleep
from typing import TypeVar

import Levenshtein  # noqa python-Levenshtein
import psutil
import pytermor as pt
import requests
from es7s_commons import UCS_CYRILLIC, GROUP_SEPARATOR, RECORD_SEPARATOR
from requests import Response

from es7s.shared import (
    get_stdout,
    get_stderr,
    Requester,
    ShutdownableThread,
    ThreadSafeCounter,
    DataCollectionError,
    get_logger,
)
from es7s.shared.uconfig import get_merged
from ._base import _BaseAction
from ._adaptive_input import _AdaptiveInputAction
from ._multi_threaded import _MultiThreadedAction


class AsciiAndCyrillicUcsTable:
    def __getitem__(self, code: int):
        if 0x1F < code < 0x7F:  # US ASCII w/o CC
            return code
        if code in UCS_CYRILLIC:
            return code
        return None


ApiResponse = dict[str, str | None]  # one for every input line, {lang_code: response_line}


@dataclass(frozen=True)
class ResultLine:  # one for every (input-line, lang_code) combo
    distance: int
    sim_ratio: float
    sim_sigma: float
    lang_code: str
    text: str


@dataclass(frozen=True)
class OutputLine:  # one for every input line
    input_line: str
    result_lines: list[ResultLine]
    most_unsimilar_lines: list[ResultLine]


class action(_MultiThreadedAction, _AdaptiveInputAction, _BaseAction):
    # fmt: off
    _LANG_CODES_ALL = {
        'af','am','ar','az','ba','be','bg','bn','bs','ca','cs','cv','cy','da','de','el','en','eo','es','et','eu','fa',
        'fi','fr','ga','gd','gu','he','hi','hr','ht','hu','hy','id','is','it','ja','ka','kk','km','kn','ko','ky','la',
        'lb','lo','lt','mg','mi','mk','ml','mn','mr','ms','mt','my','ne','nl','no','pa','pl','pt','ro','ru','si','sl',
        'sq','sr','su','sv','sw','ta','te','tg','th','th','tl','tr','tt','uk','ur','uz','vi','xh','yi','zh',
    }

    #      0 [af] Afrikaans		       22 [fi] suomi		       44 [lb] Lëtzebuergesch      66 [sq] shqip
    #      1 [am] አማርኛ		       23 [fr] français		       45 [lo] ລາວ			       67 [sr] српски
    #      2 [ar] العربية		       24 [ga] Gaeilge		       46 [lt] lietuvių		       68 [su]
    #      3 [az] azərbaycan	       25 [gd] Gàidhlig		       47 [mg] Malagasy		       69 [sv] svenska
    #      4 [ba]				       26 [gu] ગુજરાતી		       48 [mi]				       70 [sw] Kiswahili
    #      5 [be] беларуская	       27 [he] עברית		       49 [mk] македонски	       71 [ta] தமிழ்
    #      6 [bg] български		       28 [hi] हिन्दी			       50 [ml] മലയാളം		       72 [te] తెలుగు
    #      7 [bn] বাংলা			       29 [hr] hrvatski		       51 [mn] монгол		       73 [tg] тоҷикӣ
    #      8 [bs] bosanski		       30 [ht]				       52 [mr] मराठी			       74 [th] ไทย
    #      9 [ca] català		       31 [hu] magyar		       53 [ms] Melayu		       75 [th] ไทย
    #     10 [cs] čeština		       32 [hy] հայերեն	       54 [mt] Malti		       76 [tl] Filipino
    #     11 [cv]				       33 [id] Indonesia	       55 [my] မြန်မာ		       77 [tr] Türkçe
    #     12 [cy] Cymraeg		       34 [is] íslenska		       56 [ne] नेपाली		       78 [tt] татар
    #     13 [da] dansk			       35 [it] italiano		       57 [nl] Nederlands	       79 [uk] українська
    #     14 [de] Deutsch		       36 [ja] 日本語		       58 [no] norsk bokmål	       80 [ur] اردو
    #     15 [el] Ελληνικά		       37 [ka] ქართული	       59 [pa] ਪੰਜਾਬੀ		       81 [uz] o‘zbek
    #     16 [en] English		       38 [kk] қазақ тілі	       60 [pl] polski		       82 [vi] Tiếng Việt
    #     17 [eo] esperanto		       39 [km] ខ្មែរ			       61 [pt] português	       83 [xh]
    #     18 [es] español		       40 [kn] ಕನ್ನಡ			       62 [ro] română		       84 [yi] ייִדיש
    #     19 [et] eesti			       41 [ko] 한국어		       63 [ru] русский		       85 [zh] 中文
    #     20 [eu] euskara		       42 [ky] кыргызча		       64 [si] සිංහල
    #     21 [fa] فارسی		       43 [la]				       65 [sl] slovenščina

    # fmt: on

    def __init__(
        self,
        full: bool,
        all: bool,
        porcelain: bool,
        **kwargs,
    ):
        self._ippt_table = AsciiAndCyrillicUcsTable()
        kwargs.update({"auto_threads_limit": self.uconfig().get("auto-threads-limit", int)})
        super().__init__(**kwargs)

        preset_lang_codes = self.uconfig().get("preset-lang-codes", list, str)
        self._lang_codes = [preset_lang_codes, self._LANG_CODES_ALL][all]

        self._output_all = full
        self._porcelain = porcelain

        self._run()

    def _run(self):
        input_lines = self._get_input_lines()
        task_pool = TaskPool(self._lang_codes, self._threads)
        api_responses: list[ApiResponse] = task_pool.handle_tasks(input_lines)

        for output_line in self._filter_results(input_lines, api_responses):
            self._print_result(len(input_lines), output_line, self._output_all, self._porcelain)

    def _postprocess_input_line(self, s: str) -> str:
        s = super()._postprocess_input_line(s)
        s = s.strip().translate(self._ippt_table)
        s = re.sub(r"^\d+[:.)]*\s+", "", s)  # remove numerics from the start: "2. NNN" -> "NNN"
        s = re.sub(R"\s+", " ", s).strip()  # squash whitespace
        return s

    @classmethod
    def _filter_results(
        cls,
        input_lines: list[str],
        api_responses: list[ApiResponse],
    ) -> Iterable[OutputLine]:
        ttable = AsciiAndCyrillicUcsTable()

        def postprocess(s: str) -> str:
            return s.strip().translate(ttable)

        def normalize(s):
            return postprocess(s).lower()

        def compute_median(string: str, strlist: list[str], wlist: list[float]) -> str:
            n = len(string)
            # increasing the string length makes median computations unacceptably slow
            if n < 50:
                return Levenshtein.median_improve(string, strlist, wlist)
            elif n < 1000:  # empirical
                return Levenshtein.median(strlist, wlist)
            else:
                return Levenshtein.quickmedian(strlist, wlist)

        _T = TypeVar("_T")

        def try_few_indexes(elems: list[_T], *idxs: int) -> _T | None:
            for idx in [*idxs, 0]:
                try:
                    return elems[idx]
                except IndexError:
                    continue
            return None

        for idx, (input_line, line_results) in enumerate(zip(input_lines, api_responses)):
            input_line_nm = normalize(input_line)
            line_results_nm = {k: normalize(v) for k, v in line_results.items()}
            seen = {input_line_nm}

            strlist = [*line_results_nm.values(), input_line_nm]
            wlist = [0.5] * len(line_results_nm) + [1.0]
            averaged = compute_median(input_line_nm, strlist, wlist)
            filtered_lines: list[ResultLine] = []

            for lang_code, line_result in line_results.items():
                line_result_nm = line_results_nm.get(lang_code, None)
                if not line_result_nm or line_result_nm in seen:
                    continue
                seen.add(line_result_nm)

                dist = Levenshtein.distance(input_line_nm, line_result_nm)
                sim = Levenshtein.ratio(averaged, line_result_nm)
                if dist < 2 or sim < 0.30:
                    continue
                filtered_lines.append(
                    ResultLine(dist, sim, sim - 0.5, lang_code, postprocess(line_result))
                )

            sorted_by_sim_lines = sorted(filtered_lines, key=lambda ol: -ol.sim_ratio)
            sorted_by_dist_lines = sorted(filtered_lines, key=lambda ol: -ol.distance)
            sorted_by_dist_delta10 = [
                *filter(lambda rl: abs(rl.sim_sigma) < 0.10, sorted_by_dist_lines)
            ]
            most_unsimilar_lines = [
                try_few_indexes(sorted_by_sim_lines, 1),
                try_few_indexes(sorted_by_dist_delta10 or sorted_by_dist_lines, 0),
                try_few_indexes(sorted_by_sim_lines, -2, -1),
            ]
            yield OutputLine(input_line, sorted_by_sim_lines, most_unsimilar_lines)

    @classmethod
    def _print_result(
        cls,
        input_lines_count: int,
        output_line: OutputLine,
        output_all: bool,
        porcelain: bool,
    ):
        def echo_wrapped(pfx: str | None, text: str):
            pfx = pfx or ""
            msg = pfx + text
            pt.echo(msg, None, stdout.renderer, file=stdout.io, wrap=True, indent_subseq=len(pfx))

        stdout = get_stdout()
        stderr = get_stderr()
        output_is_tty = stdout.isatty()

        stderr.echoi(pt.make_set_cursor_column())
        stderr.echoi(pt.make_clear_line())  # erase progress bar
        stderr.echo("-" * 80)

        # if input_lines_count > 1:
        #     stderr.echo()
        stderr.echo(">> " + output_line.input_line)
        stderr.echo()

        lines_list = [output_line.most_unsimilar_lines, output_line.result_lines][output_all]
        for result_line in lines_list:
            if result_line:
                lang_code = result_line.lang_code[::-1].upper()
                dist = -result_line.distance
                simdiff = round(abs(result_line.sim_sigma) * 100)
                params = " ".join([f"{lang_code:2s}", f"{dist:>3d}", f"{simdiff:>+3d}%"])
                text = result_line.text
            else:
                params = "??  --  --%"
                text = "<no response>"

            prefix = None
            if output_is_tty:
                prefix = f"({params}): "

            if porcelain:
                stdout.echoi(text + RECORD_SEPARATOR)
            else:
                echo_wrapped(prefix, text)

        if porcelain:
            stdout.echoi(GROUP_SEPARATOR)


class TaskPool(BoundedSemaphore):
    _THREAD_POLL_TIME_SEC = 0.1

    def __init__(self, lang_codes: list[str], threads: int):
        super().__init__(value=threads)

        self._tasks: deque[_ApiTask] = deque()
        self._tasks_done: deque[_ApiTask] = deque()
        self._workers: deque[_ApiWorker] = deque(maxlen=threads)

        self._lang_codes = lang_codes
        self._tasks_states: list[int] = [0] * len(self._lang_codes)
        self._progress_bar = ProgressBar(self._tasks_states)

    def handle_tasks(self, input_lines: list[str]) -> list[ApiResponse]:
        self._progress_bar.redraw_event.set()
        self._progress_bar.start()

        api_responses: list[ApiResponse] = [{} for _ in range(len(input_lines))]

        for lang_code in self._lang_codes:
            task = _ApiTask(lang_code, copy(input_lines))
            self._tasks.append(task)

        for _ in range(self._workers.maxlen):
            worker = _ApiWorker(self)
            self._workers.append(worker)
            worker.start()

        while self._workers:
            needs_redraw = False
            worker: _ApiWorker = self._workers[0]
            worker.join(self._THREAD_POLL_TIME_SEC)

            while self._tasks_done:
                task = self._tasks_done.popleft()
                needs_redraw = True
                self._tasks_states[task.tasknum - 1] += 1

                if next_task := task.next_task():
                    self._tasks.appendleft(next_task)
                else:  # results are ready
                    for idx, result_line in enumerate(task.results):
                        api_responses[idx].update({task.lang_code: result_line})

            if worker.is_alive():
                self._workers.rotate()
            else:
                self._workers.remove(worker)
                needs_redraw = True

            if needs_redraw:
                self._progress_bar.redraw_event.set()

        self._progress_bar.shutdown()
        self._progress_bar.join()
        return api_responses

    @property
    def tasks(self) -> deque[_ApiTask]:
        return self._tasks

    @property
    def tasks_done(self) -> deque[_ApiTask]:
        return self._tasks_done


class ProgressBar(ShutdownableThread):
    _POLL_TIME_SEC = 0.1

    redraw_event = Event()

    def __init__(self, tasks_states: list[int]):
        super().__init__("transmorph", thread_name="ui:bar")
        self._tasks_states = tasks_states

    def run(self):
        while True:
            if self.is_shutting_down():
                self.destroy()
                return
            self.redraw_event.wait(timeout=self._POLL_TIME_SEC)
            self._redraw()

    def _redraw(self):
        self.redraw_event.clear()

        max_tasknum = 2 * len(self._tasks_states)
        finished_count = sum(self._tasks_states)
        finished_count_str = str(finished_count).rjust(len(str(max_tasknum)))
        finished_ratio_st = pt.format_auto_float(100 * finished_count / max_tasknum, 3)

        tx_before = f"Working... ({finished_count_str}/{max_tasknum}) {finished_ratio_st:>3s}% ["
        tx_after = "]"
        scale_width = pt.get_terminal_width() - (len(tx_before) + len(tx_after))
        finished_w = scale_width * finished_count // max_tasknum

        if scale_width > len(self._tasks_states):

            def getchr(state: int) -> tuple:
                return (" ▯▮"[state], [None, None, pt.cv.GREEN][state])

            scale = (*map(getchr, self._tasks_states),)
        else:
            scale = ("█" * finished_w).ljust(scale_width, "░")

        tx = pt.Text(tx_before, scale, tx_after)

        stream = get_stderr()
        if stream.sgr_allowed:
            stream.echoi(pt.make_set_cursor_column())
            stream.echoi(pt.make_clear_line())  # erase progress bar
        else:
            stream.echo()
        stream.echoi_rendered(tx)
        stream.flush()


class _ApiWorker(ShutdownableThread):
    _POLL_TIME_SEC = 0.1
    _RETRY_LIMIT = 5

    __workernum: ThreadSafeCounter = ThreadSafeCounter()

    def __init__(self, pool: TaskPool):
        self._workernum = self.__workernum.next()
        super().__init__("transmorph", thread_name=f"worker:{self._workernum}")

        self._pool = pool

    def run(self):
        from http.client import TOO_MANY_REQUESTS

        task: _ApiTask | None = None
        attempts = 0
        logger = get_logger()

        while True:
            if self.is_shutting_down():
                self.destroy()
                return

            if not task:
                if not self._pool.tasks:
                    self.shutdown()
                    continue
                if self._pool.acquire(timeout=self._POLL_TIME_SEC):
                    task = self._pool.tasks.popleft()
                    attempts = self._RETRY_LIMIT
                    self._pool.release()

            if task:
                if attempts == 0:
                    logger.warning(f"Failed to execute task #{task.tasknum} ({task.lang_code})")
                    task = None
                    continue
                try:
                    task.execute()
                except DataCollectionError as e:
                    if e.http_code == TOO_MANY_REQUESTS:
                        retry_delay = random.randint(1000, 3000) / 1e3
                        logger.debug(f"Waiting for {retry_delay:.1f}s before retrying...")
                        sleep(retry_delay)
                        attempts -= 1
                    else:
                        attempts = 0
                else:
                    self._pool.tasks_done.append(task)
                    task = None


class _ApiTask:
    _TRANSLATION_ENDPOINT_URL = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    MAX_BODY_SIZE = 10_000

    __tasknum: ThreadSafeCounter = ThreadSafeCounter()
    _requester: Requester = Requester()

    def __init__(
        self,
        lang_code: str,
        input_lines: list[str],
        *,
        _tasknum: int = None,
        _backwards: bool = False,
    ):
        self.lang_code = lang_code
        self._input_lines = input_lines
        self._tasknum = _tasknum or self.__tasknum.next()
        self._backwards = _backwards
        self._results: list[str | None] = [None] * len(self._input_lines)

    def execute(self):
        dest_code = self.lang_code
        if self._backwards:
            dest_code = get_merged().get_section("general").get("default-lang-code")

        for idx, text in enumerate(self._call_api(self._input_lines, dest_code)):
            if text is not None:
                self._results[idx] = text.strip()

    @classmethod
    def _call_api(cls: type["_ApiTask"], texts: list[str], dest_code: str) -> Iterable[str | None]:
        api_token = get_merged().get_section("auth").get("yandex-cloud-api-key")
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Api-Key {0}".format(api_token),
        }
        data = {
            "targetLanguageCode": dest_code,
            "texts": texts,
        }

        # # this parameter makes the translations more accurate - which we DON'T want,
        # # as then the output is more likely to be the same as the input:
        # if src_code:
        #     data.update({"sourceLanguageCode": src_code})

        try:
            response: Response = cls._requester.make_request(
                _ApiTask._TRANSLATION_ENDPOINT_URL,
                request_fn=lambda url: requests.post(url, json=data, headers=headers),
            )
        except DataCollectionError:
            raise

        for ts in response.json().get("translations"):
            yield ts.get("text", None)

    def next_task(self) -> t.Union["_ApiTask", None]:
        if self._backwards:
            return None
        return _ApiTask(
            self.lang_code,
            input_lines=self._results,
            _tasknum=self._tasknum,
            _backwards=True,
        )

    @property
    def tasknum(self) -> int:
        return self._tasknum

    @property
    def results(self) -> list[str | None]:
        if not self._backwards:
            raise RuntimeError("Only back translation threads can be used as final tasks")
        return self._results
