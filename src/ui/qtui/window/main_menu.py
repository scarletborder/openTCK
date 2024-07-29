import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

from src.ui.qtui.widgets.mainwindow import Ui_MainMenu  # 由mainwindow.ui生成

from src.ui.qtui.window.sub_game import SubGameMenu


class MainMenu(QMainWindow, Ui_MainMenu):
    def __init__(self):
        super().__init__()
        self.second_window = SubGameMenu()
        self.setupUi(self)

    def setupUi(self, MainMenu):
        super().setupUi(MainMenu)
        ...
