from src.constant.config.conf import Cfg
from src.utils.lobby import Lobby, PlayerInfo
from src.ui.adapter.utils import NewUI

My_Player_Info: PlayerInfo = PlayerInfo(0, "Anonymous")
Current_Lobby: Lobby | None = None
Is_Host: bool = False


def DisplayLobby():
    if Current_Lobby:
        NewUI.PrintChatArea(Current_Lobby.GetLobbyTable().get_formatted_string())
    else:
        NewUI.PrintChatArea("No available lobby")


def DisplayWhoami():
    NewUI.PrintChatArea(f"{My_Player_Info.GetId()} / {My_Player_Info.name}")
