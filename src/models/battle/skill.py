from src.constant.enum.skill import SkillType
from abc import ABC, abstractmethod


class Skill(ABC):
    # 显示信息类函数

    @abstractmethod
    def GetName(self) -> str:
        """获取技能名称"""
        ...

    @abstractmethod
    def GetDescription(self) -> str:
        """获取技能描述"""
        ...

    @abstractmethod
    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        ...

    @abstractmethod
    def GetSkillID(self): ...

    @abstractmethod
    def GetSkillType(self) -> SkillType: ...

    # 使用类
    @abstractmethod
    def JudgeLegal(self, target_id: int, times: int, game) -> bool:
        """检测技能是否参数正确"""

    @abstractmethod
    def Cast(self, caster_id: int, target_id: int, times: int, game):
        """回合结束时的结算会按次序触发每个技能的 cast 函数

        cast 函数不要管使用技能的耗费 magic point
        """
        ...
