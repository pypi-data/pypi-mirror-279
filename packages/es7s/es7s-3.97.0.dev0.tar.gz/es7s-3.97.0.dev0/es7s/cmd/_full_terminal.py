# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from __future__ import annotations

import shutil
import sys
from abc import abstractmethod
from collections import deque
from dataclasses import dataclass
from datetime import datetime
import typing as t
from functools import cached_property

import pytermor as pt
from es7s_commons import InputMode

from es7s.shared import (
    Styles as _BaseStyles,
    with_terminal_state,
    get_stdout,
    make_interceptor_io,
    IoInterceptor,
    ProxiedTerminalState,
)


class _Styles(_BaseStyles):
    def __init__(self):
        self.POPUP = pt.FrozenStyle(fg="hi-white", bg=pt.cv.NAVY_BLUE)


class Message:
    def __init__(self, text: str, ttl: float | None = 1.0):
        """
        :param text: Message text.
        :param ttl:  Duration in seconds for message to appear; specify
                     *None* to create a persistent message.
        """
        self._text = text
        self._ttl = ttl

    @property
    def text(self) -> str:
        return self._text

    def tick(self, prev_render_duration: float) -> bool:
        if self._ttl is None:
            return True
        self._ttl = max(0.0, self._ttl - prev_render_duration)
        return self._ttl > 0


class MessageQueue(deque[Message]):
    @staticmethod
    def _now_ts():
        return datetime.now().timestamp()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._prev_frame_ts = 0

    def append(self, text: str | Message):
        if isinstance(text, str):
            super().append(Message(text))
        else:
            super().append(text)

    def tick(self) -> str | None:
        prev_render_duration = self._now_ts() - self._prev_frame_ts
        self._prev_frame_ts = self._now_ts()

        while self:
            current = self[0]
            if not current.tick(prev_render_duration):
                self.popleft()
            return current.text
        return None


@dataclass(frozen=True)
class KeyListener:
    key: str
    label: str
    var: Cycleable
    callback: t.Callable = None

    @cached_property
    def hint(self) -> str:
        if self.label[0].lower() == self.key.lower():
            return f"[{self.key}]{self.label[1:]}"
        return f"[{self.key}] {self.label}"


_VT = t.TypeVar("_VT")


class Cycleable(t.Generic[_VT]):
    @property
    @abstractmethod
    def current(self) -> _VT:
        ...

    @abstractmethod
    def next(self) -> _VT:
        ...


class CycledCounter(Cycleable[int]):
    def __init__(self, max: int, min=0, init=0, step=1):
        self._max = max
        self._min = min
        self._val = init
        self._step = step
        # self._apply_limits()  # keep `init` even if it's out of bounds

    @property
    def current(self) -> int:
        return self._val

    @property
    def max(self) -> int:
        return self._max

    def set(self, val):
        self._val = val
        self._apply_limits()

    def next(self) -> int:
        self._val += self._step
        self._apply_limits()
        return self._val

    def _apply_limits(self):
        if self._val < self._min or self._val > self._max:
            self._val = (self._max, self._min)[self._step > 0]


class Toggle(Cycleable[bool]):
    def __init__(self, init=False):
        self._val = init

    @property
    def current(self) -> bool:
        return self._val

    def set(self, val: bool):
        self._val = val

    def next(self) -> bool:
        self._val = not self._val
        return self._val


_NOT_SET = object()


class CycledChoice(Cycleable[_VT]):
    def __init__(self, choices: list[_VT], *, init_idx: int = 0, init: _VT = _NOT_SET):
        """
        :param choices:    Value list.
        :param init_idx:   Initial value index, taken from `choices`. Must be a valid index.
        :param init:       Initial value, overrides `init_idx`. Not required to be in `choices`.
        """
        self._choices = choices

        self._init = self._choices[init_idx]
        if init is not _NOT_SET:
            init_idx = -1
            self._init = init
        self._counter = CycledCounter(len(self._choices) - 1, init=init_idx)

    def __str__(self):
        return f"[{self._counter.current}/{len(self._choices)-1}]"

    @property
    def current(self) -> _VT:
        current_idx = self._counter.current
        if 0 <= current_idx < len(self._choices):
            return self._choices[current_idx]
        return self._init

    def next(self) -> _VT:
        self._counter.next()
        return self.current


class _FullTerminalAction:
    KEY_QUIT = "q"
    KEY_REFRESH = "r"

    _key_listeners: list[KeyListener] = []

    def __init__(self, interval: float, **kwargs):
        super().__init__(**kwargs)

        self._interval = interval

        self._messages = MessageQueue()
        self._styles = _Styles()

        self._stdout = get_stdout()
        self._interceptor: IoInterceptor = make_interceptor_io()
        self._term_width = 0
        self._term_height = 0

    def _bind(self, label: str, var: Cycleable, callback: t.Callable = None, key: str = None):
        self._key_listeners.append(KeyListener(key or label[0], label, var, callback))
        return var

    @with_terminal_state(alt_buffer=True, no_cursor=True, input_mode=InputMode.DISABLED)
    def _main_loop(self, termstate: ProxiedTerminalState):
        import select

        while True:
            tw, th = shutil.get_terminal_size()
            if tw != self._term_width or th != self._term_height:
                self._on_terminal_resize()
                self._term_width, self._term_height = tw, th

            self._pre_render()
            self._render()
            self._post_render()
            self._stdout.echo(self._interceptor.getvalue(), nl=False)

            i, _, _ = select.select([sys.stdin], [], [], self._interval)
            if i:
                stdin = sys.stdin.read(1)
                if not stdin:
                    break
                match c := stdin[0]:
                    case self.KEY_QUIT:
                        raise SystemExit
                    case self.KEY_REFRESH:
                        continue
                    case _:
                        self._custom_keypress(c)

    def _custom_keypress(self, key: str):
        for kl in self._key_listeners:
            if key == kl.key:
                kl.var.next()
                if kl.callback:
                    kl.callback()
                return

        self._display_keys_hint()

    def _on_terminal_resize(self):
        ...

    def _display_keys_hint(self):
        self._messages.append(
            "  ".join(
                [
                    f"[{self.KEY_REFRESH}]efresh",
                    *[kl.hint for kl in self._key_listeners],
                    f"[{self.KEY_QUIT}]uit",
                ]
            )
        )

    def _pre_render(self):
        self._interceptor.reset()
        self._interceptor.echo(pt.make_reset_cursor())
        self._interceptor.echo(pt.make_clear_display())

    @abstractmethod
    def _render(self):
        raise NotImplementedError

    def _post_render(self):
        if not self._messages:
            return
        if not (message := self._messages.tick()):
            return

        popup_width = min(len(message) + 4, self._term_width)
        popup_margin = max(0, (self._term_width - popup_width) // 2)
        self._set_cursor(column=popup_margin)
        self._interceptor.echo_rendered(message.center(popup_width), self._styles.POPUP)

    def _set_cursor(self, line: int = 1, column: int = 1):
        self._interceptor.echo(pt.make_set_cursor(line=max(1, line), column=max(1, column)))
