import src.storage.lobby as SLB
from src.models.link.link_data import LobbyUpdateData
from prettytable import PrettyTable
from typing import TYPE_CHECKING
from src.constant.config.conf import Cfg, ReadComment
from src.utils.pkui.utils import NewUI

if TYPE_CHECKING:
    from src.utils.link.rpc.rpc_linker import RpcLinker


async def RunMenuCommand(s: str, Linker: "RpcLinker") -> bool:
    if s == "help":
        NewUI.PrintChatArea(
            """Menu Command
        help - Look up all menu commands.
        list - Display uids and names of players in lobby.
        skills - List all available skills.
        query [skill id|skill pinyin] - look for detailed skill description
        start - [Host only] Hold up a game and start.
        gamerule - [Host only] Modify game rules
        exit - Leave the lobby.
        """
        )
        return True

    elif s == "list":
        SLB.DisplayLobby()
        return True

    elif s == "start":
        if Linker.is_host is False:
            NewUI.PrintChatArea("host only command")
            return True

        # host下发游戏开始
        # Linker:HostPlayerLink
        await Linker.StartGame()  # type: ignore
        return True

    elif s == "whoami":
        NewUI.PrintChatArea(
            f"uid:{SLB.My_Player_Info.GetId()}/{SLB.My_Player_Info.GetName()}"
        )
        return True

    elif s == "exit":
        await LeaveGame(Linker)
        return True

    elif s == "skills":
        ListSkills()
        return True
    elif s[:5] == "query":
        if s[:6] != "query ":
            NewUI.PrintChatArea("query必须接受参数")
            return False
        keys = s[6:]
        QuerySkill(keys)
        return True
    elif s[:8] == "gamerule":
        if Linker.is_host is False:
            NewUI.PrintChatArea("host only command")
            return True
        if s[:9] != "gamerule ":
            ListGameRule()
            return True
        keys = s[9:]
        op = keys.strip().split(" ")
        if len(op) == 1:
            op.append("")
        ModifyGameRule(op[0], op[1])
        return True
        ...

    return False


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402


async def LeaveGame(Linker: "PlayerLink"):
    NewUI.PrintChatArea("你已离开游戏")
    SLB.Current_Lobby.LeavePlayer(SLB.My_Player_Info.GetId())
    await Linker.Send(LobbyUpdateData(SLB.My_Player_Info.GetId(), SLB.Current_Lobby))


def ListGameRule():
    table = PrettyTable()
    table.field_names = ["Title", "Value", "Comment"]
    for key, settings in Cfg["gamerule"].items():
        comment = ReadComment("gamerule", key)
        table.add_row([key, settings, comment])

    NewUI.PrintChatArea(table.get_formatted_string())


def QuerySkill(key):
    flag = False
    try:
        keyid = int(key)
        flag = True  # id
    except ValueError:
        ...

    if flag is False:  # id
        if key not in Skill_Name_To_ID.keys():
            NewUI.PrintChatArea("该技能不存在")
            return
        keyid = Skill_Name_To_ID[key]

    NewUI.PrintChatArea(
        f"""{keyid}-{Skill_Table[keyid].GetTitle()}-{Skill_Table[keyid].GetName()}-{Skill_Table[keyid].GetBasicPoint()}P
{Skill_Table[keyid].GetDescription()}"""
    )


def ModifyGameRule(key: str, option: str):
    def str_to_bool(s):
        if s == "True":
            return True
        elif s == "False":
            return False
        else:
            raise ValueError("Invalid input: must be 'True' or 'False'")

    if option == "":
        ops = Cfg["gamerule"].get(key, None)
        NewUI.PrintChatArea(f"\nGame Rule: {key} = {ops}\n")
    else:
        op = False
        try:
            op = str_to_bool(option)
        except ValueError as e:
            NewUI.PrintChatArea(e)

        if key not in Cfg["gamerule"].keys():
            NewUI.PrintChatArea(f"\nWarning: no option named {key}\n")

        Cfg["gamerule"][key] = op

    return True


def ListSkills():
    table = PrettyTable()
    table.field_names = ["Title", "id", "pinyin"]

    for pinyin, sid in Skill_Name_To_ID.items():
        table.add_row([Skill_Table[sid].GetTitle(), sid, pinyin])

    NewUI.PrintChatArea(table.get_formatted_string())
