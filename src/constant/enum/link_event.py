from enum import Enum


class LinkEvent(Enum):
    # 短信
    CHATMESSAGE = 0x01  # 短信发出

    # 战斗
    BATTLEACTION = 0x11  # 技能发出
    BATTLERESULT = 0x12  # 结算结果
