import asyncio
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window
from prompt_toolkit.widgets import TextArea, MenuContainer, MenuItem, Button
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.styles import Style

Input_Area = TextArea(height=1, prompt="Input: ", multiline=False)

__intro = """openTCK dev version
This program uses GPL-3.0 license
Use `ctrl + j` OR `ctrl + k` to scroll down OR up\n"""

# 主要左边的对话框，和命令的输出框
Output_Chat_Area = TextArea(
    style="class:output-area",
    focusable=False,
    scrollbar=True,
    text=__intro,
    wrap_lines=True,
)
# 主要右上的状态信息
Output_Status_Area = TextArea(
    style="class:output-area",
    focusable=False,
    scrollbar=False,
    wrap_lines=False,
    text="halo1",
)
Output_Tip_Area = TextArea(
    style="class:output-area",
    focusable=False,
    scrollbar=False,
    height=3,
    text="halo2",
)

Bindings = KeyBindings()
