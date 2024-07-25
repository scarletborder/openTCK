from src.constant.config.ui_type import UITYPE


class UIUtils:
    """UI暴露方法"""

    @staticmethod
    def PrintChatArea(s, end="\n"): ...

    @staticmethod
    def ClearChatArea(): ...

    @staticmethod
    def PrintStatusArea(s): ...

    @staticmethod
    def PrintTipArea(s): ...


NewUI = UIUtils


if UITYPE == "pkui":
    from src.ui.pkui.utils import NewUI as m

    NewUI = m
elif UITYPE == "qtui":
    from src.ui.qtui.utils import NewUI as m

    NewUI = m
else:
    print("No that UI type you required")
    exit(1)
