from asyncio import Task

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.utils.link.player_link import PlayerLink

LinkTask: Task | None = None
Linker: "PlayerLink | None" = None
