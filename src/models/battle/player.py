from typing import TYPE_CHECKING
from src.constant.enum.battle_trigger import TriggerType

if TYPE_CHECKING:
    from src.models.battle.game import Game, Skill


class Player:
    def __init__(self, Name: str = "Anonymous", id: int = 0) -> None:
        # 基本信息
        self.Name = Name
        self.id = id
        # 全局属性
        self.Health = 6
        self.Point = 0

        # 计算中属性
        self.defense_level = 0  # 防御等级，为0则为不设防
        self.health_change = 0
        self.point_change = 0
        self.is_health_change = False
        self.is_point_change = False
        self.is_hurt = False
        self.is_healed = False
        self.reset_health = False

        # 效果
        self.tag = {}

    # 显示类函数
    def __repr__(self) -> str:
        return f"<{self.id}{self.Name}>:{self.Health}/{self.Point}({self.health_change:+}/{self.point_change:+})"

    # 功能类函数
    def ChangeHealth(
        self, val: int, game: "Game|None" = None, sk_v: "Skill | None" = None
    ):
        """修改生命值
        由于部分技能会计算血量变化故单独开此函数计算玩家在回合内的血量变化

        技能 cast 时 changehealth 要把 game 和本身传入

        trigger cast时， game 和 original_skill (造成 trigger 的技能) 传入

        tips: 血量B触发器cast时获取角色之前的血量，之前的health_change

        血量P触发器cast时获取角色之前的血量，之前的health_change
        """

        if not self.is_health_change:
            self.is_health_change = True

        if val < 0:
            self.is_hurt = True
        elif val > 0:
            self.is_healed = True

        tmp_change = [val]
        if game and sk_v:
            tril = game.Trigger_Stash.misc_triggers.get(
                TriggerType.B_ONCHANGEHEALTH, []
            )
            for tri in tril:
                tri.Cast(game, sk_v, self.id, tmp_change)

        self.health_change += tmp_change[0]

        if game and sk_v:
            tril = game.Trigger_Stash.misc_triggers.get(
                TriggerType.P_ONCHANGEHEALTH, []
            )
            for tri in tril:
                tri.Cast(game, sk_v, self.id, tmp_change)

    def ResetHealth(
            self, game: "Game|None" = None, sk_v: "Skill | None" = None
    ):
        if not self.is_healed:
            self.is_healed = True

        self.reset_health = True
        
    def ChangePoint(
        self, val: int, game: "Game|None" = None, sk_v: "Skill | None" = None
    ):
        if not self.is_point_change:
            self.is_point_change = True

        tmp_change = [val]
        if game and sk_v:
            tril = game.Trigger_Stash.misc_triggers.get(TriggerType.B_ONCHANGEPOINT, [])
            for tri in tril:
                tri.Cast(game, sk_v, self.id, tmp_change)

        self.point_change += tmp_change[0]

        if game and sk_v:
            tril = game.Trigger_Stash.misc_triggers.get(TriggerType.P_ONCHANGEPOINT, [])
            for tri in tril:
                tri.Cast(game, sk_v, self.id, tmp_change)

    def OnRoundStart(self):
        """回合开始初始化数值"""
        self.defense_level = 0  # 防御等级，为0则为不设防
        self.health_change = 0
        self.point_change = 0
        self.is_health_change = False
        self.is_point_change = False

    def OnRoundEnd(self):
        """回合结束结算数值"""
        self.Health += self.health_change
        self.Point += self.point_change
        if self.reset_health:
            self.Health = 6

    # 交互类函数
