from src.constant.enum.skill import SkillType, SkillID
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.models.battle.game import Game

if TYPE_CHECKING:
    from src.models.battle.game import Game


class Skill(ABC):
    # 显示信息类函数

    def __init__(self, caster_id: int, args: list) -> None:
        self.caster_id = caster_id

    @staticmethod
    @abstractmethod
    def NewSkill(caster: int, args: list[str]) -> tuple[bool, "Skill | None", str]:
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

    @staticmethod
    def GetAttackLevel() -> int:
        return -1

    def GetTargetTimes(self, target_id: int) -> int: ...

    def GetAllTimes(self) -> int: ...

    def __str__(self) -> str:
        return f"{self.caster_id} -> {self.GetTitle()}"


class AttackSkill(Skill):
    def __init__(self, caster_id: int, args: list) -> None:
        super().__init__(caster_id, args)
        self.targets = []
        self.times = []

    @staticmethod
    def GetAttackLevel() -> int: ...


class DefenseSkill(Skill):
    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.DEFENSE


class CommandSkill(Skill):
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

    def SingleCast(self, game: Game, caster_id: int, target_id: int, times: int):
        """群体攻击对单体造成的结算"""
        ...

    def Cast(self, game: Game):
        self.targets = list(game.GetLiveUIDs())
        self.targets.remove(self.caster_id)
        self.times = [1 for _ in range(len(self.targets))]
        for idx in range(len(self.targets)):
            tid = self.targets[idx]
            times = self.times[idx]
            self.SingleCast(game, self.caster_id, tid, times)


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
