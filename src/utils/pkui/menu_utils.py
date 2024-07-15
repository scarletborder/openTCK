import asyncio
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


async def DisplaySingleSkills(): ...


async def DisplayMultiSkills(): ...


async def DisplayDefenseSkills(): ...


async def DisplayCommandSkills(): ...


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
                MenuItem("大厅列表", handler=lambda: asyncio.create_task(LobbyList())),
            ],
        ),
        MenuItem(
            "游戏",
            children=[
                MenuItem("Restart", handler=lambda: asyncio.create_task(StartGame())),
            ],
        ),
        MenuItem(
            "配置",
            children=[
                MenuItem(
                    "gamerule", handler=lambda: asyncio.create_task(DisplayGameRule())
                ),
            ],
        ),
        MenuItem(
            "帮助",
            children=[
                MenuItem(
                    "技能列表",
                    children=[
                        MenuItem(
                            "单体攻击",
                            handler=lambda: asyncio.create_task(DisplaySingleSkills()),
                        ),
                        MenuItem(
                            "群体攻击",
                            handler=lambda: asyncio.create_task(DisplayMultiSkills()),
                        ),
                        MenuItem(
                            "防御",
                            handler=lambda: asyncio.create_task(DisplayDefenseSkills()),
                        ),
                        MenuItem(
                            "指令",
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
)
