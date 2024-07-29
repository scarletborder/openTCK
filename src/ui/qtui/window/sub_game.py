import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

from src.ui.qtui.widgets.mainwindow import Ui_MainMenu  # 由mainwindow.ui生成
from src.ui.qtui.widgets.sub_game import Ui_SubGame  # 由sub_game.ui生成


class SubGameMenu(QMainWindow, Ui_SubGame):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Input_Area.toPlainText()

        # 创建定时器，每隔3秒更新一次消息
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateMessage)
        self.timer.start(3000)  # 每隔3秒触发一次

    def updateMessage(self):
        self.label.setText("hello world")
