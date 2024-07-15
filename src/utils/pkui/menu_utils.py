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


class NewUI:
    """UI暴露方法"""

    @staticmethod
    def PrintChatArea(s):
        buffer = Output_Chat_Area.buffer
        # window = output_chat_area.window

        # 检查 TextArea 是否在最低端
        is_at_bottom = buffer.document.cursor_position == len(buffer.text)

        # 在终端中运行以确保线程安全
        buffer.text += s + "\n"

        # 如果在最低端，则滚动到底部
        if is_at_bottom:
            run_in_terminal(lambda: buffer.cursor_down(len(buffer.text)))

    @staticmethod
    def PrintStatusArea(s):
        Output_Status_Area.text = s

    @staticmethod
    def PrintTipArea(s):
        Output_Tip_Area.text = s


"""联机"""


def HostLobby(): ...


def JoinLobby(): ...


def LeaveLobby(): ...


def Exit():
    App.exit()
    exit()


"""菜单

将原来的各种菜单命令移动到此处
"""


def LobbyList(): ...


"""游戏"""


def StartGame(): ...


"""配置"""


def DisplayGameRule(): ...


"""帮助"""


def DisplaySingleSkills(): ...


def DisplayMultiSkills(): ...


def DisplayDefenseSkills(): ...


def DisplayCommandSkills(): ...


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
                    handler=HostLobby,
                ),
                MenuItem(
                    "Join",
                    handler=JoinLobby,
                ),
                MenuItem("Leave", handler=LeaveLobby),
                MenuItem("Exit", handler=Exit),
            ],
        ),
        MenuItem(
            "菜单",
            children=[
                MenuItem("大厅列表", handler=LobbyList),
            ],
        ),
        MenuItem(
            "游戏",
            children=[
                MenuItem("Restart", handler=StartGame),
            ],
        ),
        MenuItem(
            "配置",
            children=[
                MenuItem("gamerule", handler=DisplayGameRule),
            ],
        ),
        MenuItem(
            "帮助",
            children=[
                MenuItem(
                    "技能列表",
                    children=[
                        MenuItem("单体攻击", handler=DisplaySingleSkills),
                        MenuItem("群体攻击", handler=DisplayMultiSkills),
                        MenuItem("防御", handler=DisplayDefenseSkills),
                        MenuItem("指令", handler=DisplayCommandSkills),
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
