import src.storage.lobby as SLB
from src.models.link.link_data import LobbyUpdateData

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.utils.link.player_link import PlayerLink, HostPlayerLink


async def RunMenuCommand(s: str, Linker: "PlayerLink") -> bool:
    if s == "help":
        print(
            """Menu Command
help - Look up all menu commands.
list - Display uids and names of players in lobby.
start - [Host only] Hold up a game and start.
exit - Leave the lobby.
"""
        )
        return True

    elif s == "list":
        print(SLB.Current_Lobby.GetLobbyTable())
        return True

    elif s == "start":
        if Linker.is_host is False:
            print("host only command")
            return True
        print("游戏开始了")
        # host下发游戏开始
        # Linker:HostPlayerLink
        await Linker.StartGame()  # type: ignore
        return True

    elif s == "whoami":
        print(f"uid:{SLB.My_Player_Info.GetId()}/{SLB.My_Player_Info.GetName()}")
        return True

    elif s == "exit":
        print("你已离开游戏")
        SLB.Current_Lobby.LeavePlayer(SLB.My_Player_Info.GetId())
        await Linker.Send(
            LobbyUpdateData(SLB.My_Player_Info.GetId(), SLB.Current_Lobby)
        )
        return True

    return False
