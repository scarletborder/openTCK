import asyncio
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window
from prompt_toolkit.widgets import TextArea, MenuContainer, MenuItem, Button
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.styles import Style

from src.ui.pkui.menu_utils import App
import src.ui.pkui.keybindings as _


async def Main():
    await App.run_async()
