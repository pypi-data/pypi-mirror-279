# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
import pickle
import sys
from threading import Event

from es7s.shared import SocketClient, get_stdout, inspect
from es7s.shared import get_socket_path, get_logger
from es7s.shared.enum import SocketTopic
from ._base import _BaseAction


class action_list(_BaseAction):
    def __init__(self, **kwargs):
        self._run()

    def _run(self):
        for topic in SocketTopic.list():
            get_stdout().echo(topic)


class action_path(_BaseAction):
    def __init__(self, **kwargs):
        self._run(**kwargs)

    def _run(self, topic: str):
        path: str = get_socket_path(topic)
        if not os.path.exists(path):
            get_logger().warning(f"File does not exist: {path!r}")
        get_stdout().echo(path)


class action_read(_BaseAction):
    def __init__(self, topic: str, raw: bool):
        self._socket_client = SocketClient(None, 0, Event(), Event(), topic, topic)
        self._run(raw)

    def _run(self, raw: bool):
        data = self._socket_client.read_once()
        if raw:
            sys.stdout.buffer.write(data)
            sys.stdout.flush()
        else:
            try:
                dto = pickle.loads(data)
                get_stdout().echo(inspect(dto.data))
            except Exception as e:
                raise RuntimeError(f"Failed to deserialize data: {e}, {data!r}") from e
