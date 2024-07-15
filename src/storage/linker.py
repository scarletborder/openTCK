from asyncio import Task

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.utils.link.player_link import PlayerLink

import threading


class Once:
    def __init__(self):
        self._lock = threading.Lock()
        self._has_run = False

    def do(self, func):
        if not self._has_run:
            with self._lock:
                if not self._has_run:
                    func()
                    self._has_run = True


LinkTask: Task | None
GlobalLinker: "PlayerLink | None"


def init():
    global LinkTask, GlobalLinker
    GlobalLinker = None
    LinkTask = None


once = Once()
once.do(init)
