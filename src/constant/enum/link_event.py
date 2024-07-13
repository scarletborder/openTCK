from enum import Enum


class LinkEvent(Enum):
    # 短信
    CHATMESSAGE = 0x01  # 短信发出

    # 大厅
    LOBBYUPDATE = 0x41  # 大厅更新，只支持完整的大厅对象
    LOBBYASSIGN = 0x42  # host为client分配一个uid

    # 战斗
    BATTLEACTION = 0x11  # 技能发出
    BATTLERESULT = 0x12  # 结算结果
    BATTLESTART = 0x13  # 游戏开始
