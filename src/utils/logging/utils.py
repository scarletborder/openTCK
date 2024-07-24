from src.utils.pkui.utils import NewUI


def Errorln(msg: str):
    NewUI.PrintChatArea("[ERROR]" + msg)


def Warnln(msg: str):
    NewUI.PrintChatArea("[WARN]" + msg)


def Infoln(msg: str):
    NewUI.PrintChatArea("[INFO]" + msg)
