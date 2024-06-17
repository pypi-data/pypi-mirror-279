# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing


class ExecutableNotFoundError(RuntimeError):
    def __init__(self, path: str, msg: str = None) -> None:
        self._path = path
        if not msg:
            msg = f"Exit code 127 (probably subprocess issue) by: {path!r}"
        super().__init__(msg)


class ArgCountError(Exception):
    def __init__(self, actual: int, *expected: int) -> None:
        expected_str = ", ".join(str(e) for e in expected)
        msg = f"Invalid arguments amount, expected one of: ({expected_str}), got: {actual}"
        super().__init__(msg)


class DataCollectionError(Exception):
    def __init__(self, msg: str = "Data collection failed", http_code: int = None):
        self._msg = msg
        self._http_code = http_code

    @property
    def msg(self) -> str:
        return self._msg

    @property
    def http_code(self) -> int | None:
        return self._http_code


class SubprocessExitCodeError(RuntimeError):
    def __init__(self, exit_code: int, args: typing.Iterable) -> None:
        from es7s_commons import format_attrs

        super().__init__(
            f"Subprocess terminated with exit code {exit_code}. Command was {format_attrs(args)}"
        )


class AutodiscoverValidationError(Exception):
    def __init__(self, cfg_path: str, *error_msg: str):
        errnum = len(error_msg)
        msg = "\n\t".join([f"Autoconfig {cfg_path!r} is invalid (x{errnum}):", *error_msg])
        super().__init__(msg)
