class Player:
    def __init__(self) -> None:
        # 基本信息
        self.Name = ""
        self.No = 0
        # 战斗属性
        self.Health = 5
        self.Point = 0
        self.health_change = 0
        self.point_change = 0
        self.is_health_change = False
        self.is_point_change = False
        # 效果

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

    def OnRoundStart():
        """回合开始初始化数值"""
        ...

    def OnRoundEnd():
        """回合结束结算数值"""
        ...
