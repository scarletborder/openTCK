import asyncio

from src.ui.qtui.window.main_menu import MainMenu

from src.ui.qtui.slots.main_menu.buttons import *


def ConnectHost(ui: MainMenu):
    ui.Host_btn.clicked.connect(startButtonClicked)


def ConnectClient(ui: MainMenu):
    ui.Client_btn.clicked.connect(startButtonClicked)


def ConnectTutorial(ui: MainMenu): ...


def ConnectConfigure(ui: MainMenu): ...


def ConnectSlots(ui: MainMenu):
    # 连接各种按钮
    ConnectHost(ui)
    ConnectClient(ui)
    ConnectTutorial(ui)
    ConnectConfigure(ui)
