from src.constant.config.conf import Cfg
from src.utils.lobby import Lobby, PlayerInfo
from src.utils.pkui.utils import NewUI

My_Player_Info: PlayerInfo = PlayerInfo(0, "Anonymous")
Current_Lobby: Lobby
Is_Host: bool = False


def DisplayLobby():
    NewUI.PrintChatArea(Current_Lobby.GetLobbyTable().get_formatted_string())


def DisplayWhoami():
    NewUI.PrintChatArea(f"{My_Player_Info.GetId()} / {My_Player_Info.name}")
