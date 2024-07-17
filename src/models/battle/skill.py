from src.constant.enum.skill import SkillType, SkillID
from src.constant.enum.skill_modified_info import SkillModifiedInfo
from src.constant.enum.battle_tag import TagEvent
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
import types

if TYPE_CHECKING:
    from src.models.battle.game import Game


class Skill(ABC):
    # 显示信息类函数

    def __init__(self, caster_id: int, args: list) -> None:
        self.caster_id = caster_id
        self.modified_info = []  # 二维list，第一维为str，第二维为属性值

    @staticmethod
    @abstractmethod
    def NewSkill(
        caster: int, args: list[str], game: "Game|None" = None
    ) -> tuple[bool, "Skill | None", str]:
        """字符串参数是否正确，并导出一个实例化"""
        ...

    @staticmethod
    @abstractmethod
    def GetTitle() -> str:
        """获取技能中文名称"""
        ...

    @staticmethod
    @abstractmethod
    def GetName() -> str:
        """获取技能拼音名称"""
        ...

    @staticmethod
    @abstractmethod
    def GetDescription() -> str:
        """获取技能描述"""
        ...

    @staticmethod
    @abstractmethod
    def GetBasicPoint() -> int:
        """获取一次技能释放需要耗费的基础点数"""
        ...

    @staticmethod
    @abstractmethod
    def GetSkillID() -> SkillID: ...

    @staticmethod
    @abstractmethod
    def GetSkillType() -> SkillType: ...

    @abstractmethod
    def GetPoint(self) -> int:
        """获取技能释放需要耗费的全部点数"""
        ...

    # 使用类

    @abstractmethod
    def Cast(self, game: "Game"):
        """回合结束时的结算会按次序触发每个技能的 cast 函数

        cast 函数不要管使用技能的耗费 magic point
        """
        ...

    def SetCast(self, new_cast_func):
        """new_cast_func是新的cast方法，需要接受(self,game)作为参数"""

        self.Cast = types.MethodType(new_cast_func, self)

    def SetModifiedInfo(self, new_record: list[SkillModifiedInfo, Any]):
        """new_record是一个长度为2的一维列表，其中第一维是SkillModifiedInfo决定的int，第二维是属性值"""
        self.modified_info.append(new_record)

    def UnableCast(self):
        def blank(game: "Game"):
            return

        self.SetCast(blank)

    @staticmethod
    def GetAttackLevel() -> int:
        return -1

    def GetTargetTimes(self, target_id: int) -> int: ...

    def GetAllTimes(self) -> int: ...

    def __str__(self) -> str:
        return f"{self.caster_id} -> {self.GetTitle()}"

    # utils
    @staticmethod
    def ParseItemModifiedInfo(
        modified_info: list[list], item: SkillModifiedInfo
    ) -> list:
        """
        解析Modified Info中为Item的参数，返回所有符合条件的参数列表
        """
        return [i[1] for i in modified_info if i[0] == item]


class AttackSkill(Skill):
    def __init__(self, caster_id: int, args: list) -> None:
        super().__init__(caster_id, args)
        self.targets = []
        self.times = []

    def SetTarget(self, new_target: list[int]):
        """用于trigger修改原技能的target"""
        self.targets = new_target

    @staticmethod
    def GetAttackLevel() -> int: ...

    def IsValidToTarget(self, target_id: int, game: "Game|None" = None) -> bool:
        # 1. 检查是否被无效化
        _ = self.ParseItemModifiedInfo(
            self.modified_info, SkillModifiedInfo.INVALIDATED
        )
        if (self.caster_id, target_id) in _:
            return False

        return True


class DefenseSkill(Skill):
    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.DEFENSE


class CommandSkill(Skill):
    """所有指令技能会进入一个列表，再收集完所有指令技能后会进行排序
    在game result处理之时
    """

    @staticmethod
    def GetCmdOccasion() -> int:
        """指令技能的使用时机

        1 - 回合开始后

        4 - 攻击技能结算后
        """
        return 9

    def CouldCmdCast(self, occ: int) -> bool:
        return occ == self.GetCmdOccasion()

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.COMMAND


class MultiAttackSkill(AttackSkill):
    def __init__(self, caster_id: int, args: list) -> None:
        super().__init__(caster_id, args)
        self.targets = []
        self.times = []

    def GetTargetTimes(self, target_id: int) -> int:
        """对目标使用了多少次技能"""
        return 1
        # try:
        #     idx = self.targets.index(target_id)
        # except ValueError:
        #     idx = -1

        # if idx < 0:
        #     return 0
        # return self.times[idx]

    def GetAllTimes(self) -> int:
        """获得使用技能的所有次数"""
        return sum(self.times)

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.MULTI

    def SingleCast(self, game: "Game", caster_id: int, target_id: int, times: int):
        """群体攻击对单体造成的结算"""
        ...


class SingleAttackSkill(AttackSkill):
    def __init__(self, caster_id: int, args: list) -> None:
        """args为偶数个，[0]为目标，[1]为次数"""
        super().__init__(caster_id, args)
        pos = 0
        self.targets = []
        self.times = []

        while pos + 1 < len(args):
            self.targets.append(args[pos])
            self.times.append(args[1 + pos])
            pos += 2

    def __str__(self) -> str:
        s = ""
        for idx in range(len(self.targets)):
            s += f"{self.targets[idx]}({self.times[idx]} Times)  "
        return f"{self.caster_id} -{self.GetTitle()}> {s}"

    def GetTargetTimes(self, target_id: int) -> int:
        """对目标使用了多少次技能"""
        try:
            idx = self.targets.index(target_id)
        except ValueError:
            idx = -1

        if idx < 0:
            return 0
        return self.times[idx]

    def GetAllTimes(self) -> int:
        """获得使用技能的所有次数"""
        return sum(self.times)

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.SINGLE
