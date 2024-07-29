import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

from src.ui.qtui.widgets.mainwindow import Ui_MainMenu  # 由mainwindow.ui生成
from src.ui.qtui.widgets.sub_game import Ui_SubGame  # 由sub_game.ui生成


from src.ui.qtui.window.main_menu import MainMenu


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainMenu()
    main_window.show()
    sys.exit(app.exec())


async def Main():
    await App.run_async()
