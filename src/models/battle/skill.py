from src.enum.skill import SkillType
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
    def GetSkillType(self) -> SkillType: ...

    # 使用类
    @abstractmethod
    def JudgeLegal(self, target_id: int, times: int) -> bool:
        """检测技能是否参数正确"""

    @abstractmethod
    def Cast(self, caster_id: int, target_id: int, times: int):
        """在结算时候的释放技能"""
        ...
