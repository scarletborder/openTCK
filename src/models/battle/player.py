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
        # 效果

    # 显示类函数
    def __repr__(self) -> str:
        return f"<{self.id}{self.Name}>:{self.Health}/{self.Point}({self.health_change:+}/{self.point_change:+})"

    # 功能类函数
    def ChangeHealth(self, val: int):
        """修改生命值
        由于部分技能会计算血量变化故单独开此函数计算玩家在回合内的血量变化
        """
        if not self.is_health_change:
            self.is_health_change = True
        self.health_change += val

    def ChangePoint(self, val: int):
        if not self.is_point_change:
            self.is_point_change = True
        self.point_change += val

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

    # 交互类函数
