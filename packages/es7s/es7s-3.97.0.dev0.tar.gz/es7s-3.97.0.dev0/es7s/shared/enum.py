# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import enum

import pytermor as pt


class _StrEnum(str, pt.ExtendedEnum):
    def __str__(self):
        return self.value


class RepeatedMode(str, pt.ExtendedEnum):
    """print-bin"""

    ACTIVE = "active"
    GROUPS = "groups"
    ALL = "all"


class MarginMode(str, enum.Enum):
    """print-env"""

    FULL = "full"
    HALF = "half"
    NONE = "none"

    def __str__(self):
        return self.value


class QuoteMode(str, enum.Enum):
    """print-env"""

    ALWAYS = "always"
    NEVER = "never"
    AUTO = "auto"

    def __str__(self):
        return self.value


class EsqDbMode(str, enum.Enum):
    SEND = "send"
    RECV = "recv"

    def __str__(self):
        return self.value


class PrintFfmpegMode(str, pt.ExtendedEnum):
    CODECS = "codecs"
    ENCODERS = "encoders"
    DECODERS = "decoders"


class SocketTopic(str, pt.ExtendedEnum):
    BATTERY = "battery"
    CPU = "cpu"
    DATETIME = "datetime"
    DISK_IO = "disk-io"
    DISK_USAGE = "disk-usage"
    DISK_MOUNTS = "disk-mounts"
    DOCKER = "docker"
    FAN = "fan"
    LOGINS = "logins"
    MEMORY = "memory"
    NETWORK_COUNTRY = "network-country"
    NETWORK_LATENCY = "network-latency"
    NETWORK_USAGE = "network-usage"
    SHOCKS = "shocks"
    SYSTEMCTL = "systemctl"
    TEMPERATURE = "temperature"
    TIMESTAMP = "timestamp"
    VOLTAGE = "voltage"
    WEATHER = "weather"


class FilterType(str, enum.Enum):  # @TODO str enums will be available in python 3.11
    OFF = "off"
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"

    def __str__(self):
        return self.value


class SelectorType(str, enum.Enum):  # @TODO str enums will be available in python 3.11
    FIRST = "first"
    CYCLE = "cycle"

    def __str__(self):
        return self.value


class EventStyle(str, enum.Enum):  # @TODO str enums will be avilable in python 3.11
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"

    @property
    def filename(self) -> str:
        return EventIconMap().get(self, "info")

    def __str__(self):
        return self.value


class EventIconMap(dict):
    def __init__(self):
        super().__init__(
            {
                EventStyle.INFO: "info",
                EventStyle.WARNING: "emblem-ohno",
                EventStyle.ERROR: "dialog-close",
                EventStyle.SUCCESS: "dialog-ok",
            }
        )


class RulerType(str, pt.ExtendedEnum):  # @TODO str enums will be available in python 3.11
    TOP = "T"
    BOTTOM = "B"
    LEFT = "L"
    RIGHT = "R"
    CENTER_HORIZONTAL = "CH"

    def __str__(self):
        return self.value

    @classmethod
    def DEFAULT(cls):
        return [cls.TOP, cls.BOTTOM, cls.LEFT, cls.RIGHT]


class KeysMode(_StrEnum):
    TMUX = "tmux"
    X11 = "x11"
    GIMP = "gimp"
    NANO = "nano"


class GraphOutputFormat(_StrEnum):
    CLI = "cli"
    DOT = "dot"
    SVG = "svg"
    PNG = "png"


class WordType(_StrEnum):
    NOUN = "noun"
    ADJ = "adj"
    VERB = "verb"
    DPART = "dpart"
    OTHER = "other"

    @staticmethod
    def styles() -> dict:
        return {
            WordType.NOUN: pt.FrozenStyle(fg=pt.cv.GREEN),
            WordType.ADJ: pt.FrozenStyle(fg=pt.cv.YELLOW),
            WordType.VERB: pt.FrozenStyle(fg=pt.cv.BLUE),
            WordType.DPART: pt.FrozenStyle(fg=pt.cv.CYAN),
            WordType.OTHER: pt.FrozenStyle(fg=pt.cv.GRAY_50),
        }
