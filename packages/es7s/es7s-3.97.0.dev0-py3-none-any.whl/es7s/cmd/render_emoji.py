# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from es7s_commons.progressbar import ProgressBar

from es7s.shared import sub, get_stdout, get_logger
from es7s.shared.decorators import with_progress_bar
from ._base import _BaseAction


@with_progress_bar(task_label="Rendering file")
class action(_BaseAction):
    def __init__(self, pbar: ProgressBar, font: str, size: int, output: str, char: tuple[str], **kwargs):
        import emoji.core

        if not char:
            char = emoji.core.distinct_emoji_list('🐍🙈🧊')

        get_stdout().echo_rendered("")

        self._pbar = pbar
        self._run(font, size, output, "".join(char))

    def _run(self, font: str, size: int, out_filename_tpl: str, chars: str) -> tuple[int, int]:
        from emoji import distinct_emoji_list

        size_norm = 80000    # originally 20000
        emojis = distinct_emoji_list(chars)
        success, total = 0, len(emojis)
        self._pbar.init_steps(steps_amount=total)

        for idx, emoji in enumerate(emojis):
            filename = f"{out_filename_tpl}.png" % emoji

            args = [
                "convert", "-background", "transparent", "-size", "%sx%s" % (size, size),
                "-set", "colorspace", "sRGB",
                "pango:<span font=\"%s\" size=\"%d\">%s</span>" % (font, size_norm, emoji),
                filename
            ]
            exitcode = sub.run_detached(args)
            if exitcode != 0:
                get_logger().error(f"Failed to write {filename!r}, exit code: {exitcode}")
            else:
                success += 1
                get_stdout().echo(f"Wrote file: {filename!r}")
            self._pbar.next_step(step_label=f'{filename}')
        return success, total
