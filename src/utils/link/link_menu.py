from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.utils.link.player_link import PlayerLink


def RunMenuCommand(s: str, Linker: "PlayerLink") -> bool:
    if s == "help":
        print(
            """Menu Command
help - Look up all menu commands.
start - [Host only] Hold up a game and start.
"""
        )
        return True

    elif s == "start":
        if Linker.is_host is False:
            print("host only command")
            return True
        print("游戏开始了")
        # host下发游戏开始
        return True
    return False
