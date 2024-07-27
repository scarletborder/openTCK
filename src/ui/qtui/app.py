import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

from src.ui.qtui.widgets.mainwindow import Ui_MainMenu  # 由mainwindow.ui生成
from src.ui.qtui.widgets.sub_game import Ui_SubGame  # 由sub_game.ui生成


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 设置Logo图片
        self.logo_label.setPixmap(
            QPixmap("path_to_your_logo.png")
        )  # 替换为你的Logo路径

        # 连接开始按钮
        self.start_button.clicked.connect(self.startButtonClicked)

    def startButtonClicked(self):
        self.second_window = SecondWindow()
        self.second_window.show()
        self.close()


class SecondWindow(QMainWindow, Ui_SecondWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 创建定时器，每隔3秒更新一次消息
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateMessage)
        self.timer.start(3000)  # 每隔3秒触发一次

    def updateMessage(self):
        self.label.setText("hello world")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
