import shutil
import asyncio
import tomlkit
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window
from prompt_toolkit.widgets import TextArea, MenuContainer, MenuItem, Button
from prompt_toolkit.application.run_in_terminal import run_in_terminal
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.styles import Style

from src.utils.pkui.widgets import (
    Input_Area,
    Output_Chat_Area,
    Output_Status_Area,
    Output_Tip_Area,
    Bindings,
)
from src.utils.pkui.utils import NewUI
from src.utils.link.player_link import HostPlayerLink
from src.utils.link.player_link import ClientPlayerLink
from src.storage.linker import LinkTask, GlobalLinker
import src.utils.link.link_menu as LMM

from src.constant.enum.skill import SkillType
from prettytable import PrettyTable
from src.battle.skills import Skill_Name_To_ID, Skill_Table

"""联机"""


async def HostLobby():
    global LinkTask, GlobalLinker
    if LinkTask is not None:
        NewUI.PrintChatArea("你已经在一场游戏中或尝试连接中")
    else:
        GlobalLinker = HostPlayerLink()
        LinkTask = asyncio.create_task(GlobalLinker.JoinLobby())


async def JoinLobby():
    global LinkTask, GlobalLinker
    if LinkTask is not None:
        NewUI.PrintChatArea("你已经在一场游戏中或尝试连接中")
    else:
        GlobalLinker = ClientPlayerLink()
        LinkTask = asyncio.create_task(GlobalLinker.JoinLobby())


async def LeaveLobby():
    global GlobalLinker, LinkTask
    if LinkTask is not None and GlobalLinker is not None:
        try:
            await LMM.LeaveGame(GlobalLinker)
        except BaseException:
            ...
        LinkTask.cancel()
        LinkTask = None
        GlobalLinker = None
    else:
        NewUI.PrintChatArea("你已经退出了一场游戏")


async def Exit():
    App.exit()
    # exit()


"""菜单

将原来的各种菜单命令移动到此处
"""


async def LobbyList():
    if LinkTask is not None and GlobalLinker is not None:
        await LMM.RunMenuCommand("list", GlobalLinker)
    else:
        NewUI.PrintChatArea("你已经退出了一场游戏")


"""游戏"""


async def StartGame():
    if LinkTask is not None and GlobalLinker is not None:
        await LMM.RunMenuCommand("start", GlobalLinker)
    else:
        NewUI.PrintChatArea("你已经退出了一场游戏")


"""配置"""


async def DisplayGameRule():
    LMM.ListGameRule()


"""帮助"""


async def DisplayAbout():
    with open("doc/help/about.txt", mode="r", encoding="utf-8") as file:
        NewUI.PrintChatArea(file.read())


async def DisplayBasicRules():
    with open("doc/help/basic.txt", mode="r", encoding="utf-8") as file:
        NewUI.PrintChatArea(file.read())


async def DisplaySingleSkills():
    table = PrettyTable()
    table.field_names = ["Title", "id", "pinyin", "Point"]

    for pinyin, sid in Skill_Name_To_ID.items():
        sk = Skill_Table[sid]
        if sk.GetSkillType() == SkillType.SINGLE:
            table.add_row([sk.GetTitle(), sid, pinyin, sk.GetBasicPoint()])

    NewUI.PrintChatArea(table.get_formatted_string())


async def DisplayMultiSkills():
    table = PrettyTable()
    table.field_names = ["Title", "id", "pinyin", "Point"]

    for pinyin, sid in Skill_Name_To_ID.items():
        sk = Skill_Table[sid]
        if sk.GetSkillType() == SkillType.MULTI:
            table.add_row([sk.GetTitle(), sid, pinyin, sk.GetBasicPoint()])

    NewUI.PrintChatArea(table.get_formatted_string())


async def DisplayDefenseSkills():
    table = PrettyTable()
    table.field_names = ["Title", "id", "pinyin", "Point"]

    for pinyin, sid in Skill_Name_To_ID.items():
        sk = Skill_Table[sid]
        if sk.GetSkillType() == SkillType.DEFENSE:
            table.add_row([sk.GetTitle(), sid, pinyin, sk.GetBasicPoint()])

    NewUI.PrintChatArea(table.get_formatted_string())


async def DisplayCommandSkills():
    table = PrettyTable()
    table.field_names = ["Title", "id", "pinyin", "Point"]

    for pinyin, sid in Skill_Name_To_ID.items():
        sk = Skill_Table[sid]
        if sk.GetSkillType() == SkillType.COMMAND:
            table.add_row([sk.GetTitle(), sid, pinyin, sk.GetBasicPoint()])

    NewUI.PrintChatArea(table.get_formatted_string())


async def ClearChatArea():
    NewUI.ClearChatArea()


async def ResetConfig():
    global Cfg
    try:
        shutil.copy("src/constant/config/configtemplate.toml", "config.toml")
        NewUI.PrintChatArea("现在你可以重新打开软件进行读取配置")
    except BaseException as e:
        NewUI.PrintChatArea("could not copy config file" + str(e))


Menu = MenuContainer(
    body=HSplit(
        [
            VSplit(
                [
                    Output_Chat_Area,
                    HSplit(
                        [
                            Output_Status_Area,
                            Window(height=1, char="-", style="class:line"),
                            Output_Tip_Area,
                        ]
                    ),
                ]
            ),
            Window(height=1, char="-", style="class:line"),  # 水平分割线
            Input_Area,
        ]
    ),
    menu_items=[
        MenuItem(
            "联机",
            children=[
                MenuItem(
                    "Host",
                    handler=lambda: asyncio.create_task(HostLobby()),
                ),
                MenuItem(
                    "Join",
                    handler=lambda: asyncio.create_task(JoinLobby()),
                ),
                MenuItem("Leave", handler=lambda: asyncio.create_task(LeaveLobby())),
                MenuItem("Exit", handler=lambda: asyncio.create_task(Exit())),
            ],
        ),
        MenuItem(
            "菜单",
            children=[
                MenuItem("Lobby", handler=lambda: asyncio.create_task(LobbyList())),
            ],
        ),
        MenuItem(
            "游戏",
            children=[
                MenuItem(
                    "ClearWindow", handler=lambda: asyncio.create_task(ClearChatArea())
                ),
                MenuItem("Restart", handler=lambda: asyncio.create_task(StartGame())),
            ],
        ),
        MenuItem(
            "配置",
            children=[
                MenuItem("reset", handler=lambda: asyncio.create_task(ResetConfig())),
                MenuItem(
                    "gamerule", handler=lambda: asyncio.create_task(DisplayGameRule())
                ),
            ],
        ),
        MenuItem(
            "帮助",
            children=[
                MenuItem("about", handler=lambda: asyncio.create_task(DisplayAbout())),
                MenuItem(
                    "BasicRules",
                    handler=lambda: asyncio.create_task(DisplayBasicRules()),
                ),
                MenuItem(
                    "Skills",
                    children=[
                        MenuItem(
                            "SingleAttack",
                            handler=lambda: asyncio.create_task(DisplaySingleSkills()),
                        ),
                        MenuItem(
                            "MultiAttack",
                            handler=lambda: asyncio.create_task(DisplayMultiSkills()),
                        ),
                        MenuItem(
                            "Defense",
                            handler=lambda: asyncio.create_task(DisplayDefenseSkills()),
                        ),
                        MenuItem(
                            "Command",
                            handler=lambda: asyncio.create_task(DisplayCommandSkills()),
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# 创建应用程序
App = Application(
    layout=Layout(Menu),
    key_bindings=Bindings,
    full_screen=True,
    color_depth=ColorDepth.TRUE_COLOR,
    mouse_support=True,
)
