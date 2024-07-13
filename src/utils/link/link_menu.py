import src.storage.lobby as SLB
from src.models.link.link_data import LobbyUpdateData
from prettytable import PrettyTable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.utils.link.player_link import PlayerLink, HostPlayerLink


async def RunMenuCommand(s: str, Linker: "PlayerLink") -> bool:
    if s == "help":
        print(
            """Menu Command
help - Look up all menu commands.
list - Display uids and names of players in lobby.
skills - List all available skills.
query [skill id|skill pinyin] - look for detailed skill description
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

    elif s == "skills":
        ListSkills()
        return True
    elif s[:6] == "query ":
        keys = s[6:]
        QuerySkill(keys)
        return True

    return False


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402


def QuerySkill(key):
    flag = False
    try:
        keyid = int(key)
        flag = True  # id
    except ValueError:
        ...

    if flag is False:  # id
        if key not in Skill_Name_To_ID.keys():
            print("该技能不存在")
            return
        keyid = Skill_Name_To_ID[key]

    print(
        f"""{keyid}-{Skill_Table[keyid].GetTitle()}-{Skill_Table[keyid].GetName()}-{Skill_Table[keyid].GetBasicPoint()}P
{Skill_Table[keyid].GetDescription()}"""
    )


def ListSkills():
    table = PrettyTable()
    table.field_names = ["Title", "id", "pinyin"]

    for pinyin, sid in Skill_Name_To_ID.items():
        table.add_row([Skill_Table[sid].GetTitle(), sid, pinyin])

    print(table)
