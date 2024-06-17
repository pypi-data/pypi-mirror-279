# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re

import pytermor as pt
from es7s_commons import WeatherIconSet, WEATHER_ICON_SETS, get_wicon, justify_wicon

from es7s.shared import get_stdout, uconfig
from ._base import _BaseAction


class action(_BaseAction):
    """
    Print weather icons used in `es7s/monitor`.
    """

    PAD = " " * 1

    def __init__(self, **kwargs):
        self._run(**kwargs)

    def _run(self, measure: bool, **kwargs):
        uc = uconfig.get_merged().get_section("monitor.weather")
        max_width = uc.get("weather-icon-max-width", int)
        
        result = "inp|"
        for set_id in range(WeatherIconSet.MAX_SET_ID + 1):
            set_idstr = f"s{set_id}".center(max_width)
            result += set_idstr + "|"

        sepm = "|" + re.sub("[^|]", "=", result[1:])
        sepb = re.sub("=", "_", sepm)
        sept = "." + re.sub("\|", "_", sepb[1:-1]) + "."

        stdout = get_stdout()
        stdout.echo(self.PAD + sept)
        stdout.echo_rendered(self.PAD + result)
        stdout.echo(self.PAD + sepm)

        for origin in WEATHER_ICON_SETS.keys():
            renders = ["|"]
            measurements = []
            for set_id in range(-1, WeatherIconSet.MAX_SET_ID + 1):
                icon, term, style = get_wicon(origin, set_id)
                justified, real_width = justify_wicon(icon, max_width, measure)
                if measure:
                    justified = justified.replace(
                        "␣", f"{pt.SeqIndex.INVERSED}␣{pt.SeqIndex.INVERSED_OFF}"
                    )
                    measurements += [real_width]
                term += pt.SeqIndex.RESET.assemble()
                renders += [stdout.render(justified + term + "|", style)]

            stdout.echo(self.PAD, nl=False)
            for render in renders:
                stdout.echo(render, nl=False)

            for measurement in measurements:
                stdout.echo("  ", nl=False)
                stdout.echo(measurement, nl=False)

            stdout.echo()
        stdout.echo(self.PAD + sepb)
