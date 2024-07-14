from enum import Enum


class TriggerType(Enum):
    ROUNDSTART = 1  # 回合开始
    ROUNDEND = 2  # 回合结束

    B_SPECIFIEDSKILL = 11  # 使用特定技能之前
    P_SPECIFEDSKILL = 12  # 之后

    B_ATTACKSKILL = 13  # 使用了攻击性技能
    P_ATTACKSKILL = 14

    B_ONCHANGEHEALTH = 21  # 血量改变
    P_ONCHANGEHEALTH = 22
    B_ONCHANGEPOINT = 21  # 点数改变
    P_ONCHANGEPOINT = 22

    B_SPECIFIEDPLAYER = 31  # 特定玩家使用技能
    P_SPECIFIEDPLAYER = 32
