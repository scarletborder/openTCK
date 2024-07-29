from src.ui.qtui.window.sub_game import SubGameMenu
from src.ui.qtui.window.main_menu import MainMenu
import webbrowser


def startButtonClicked(self: MainMenu):
    self.second_window.show()
    self.close()


def OpenTutorial(self: MainMenu):
    # 要访问的网页 URL
    url = "https://scarletborder.cn/blog/tck_readme"

    # 启动默认浏览器并打开指定的 URL
    webbrowser.open(url)


def OpenConfigure(self: MainMenu): ...
