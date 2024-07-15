import asyncio
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window
from prompt_toolkit.widgets import TextArea, MenuContainer, MenuItem, Button
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.styles import Style
from prompt_toolkit.application.run_in_terminal import run_in_terminal

from src.utils.pkui.widgets import (
    Input_Area,
    Output_Chat_Area,
    Output_Status_Area,
    Output_Tip_Area,
    Bindings,
)

from src.utils.pkui.menu_utils import NewUI


@Bindings.add("c-c")
@Bindings.add("c-q")
def _(event):
    event.app.exit()


@Bindings.add("c-k")
def ScrollUp(event):
    Output_Chat_Area.buffer.cursor_up(
        count=len(Output_Chat_Area.window.render_info.displayed_lines) // 2
    )


@Bindings.add("c-j")
def ScrollDown(event):
    Output_Chat_Area.buffer.cursor_down(
        count=len(Output_Chat_Area.window.render_info.displayed_lines) // 2
    )


@Bindings.add("tab")
def FocusNextt(event):
    event.app.layout.focus_next()


@Bindings.add("enter")
def InputConfirm(event):
    # 获取输入内容并清除输入框
    input_text = Input_Area.text
    Input_Area.text = ""
    NewUI.PrintChatArea(input_text)
