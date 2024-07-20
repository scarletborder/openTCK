from src.models.battle.skill import CommandSkill, Skill
from src.constant.enum.skill import SkillType, SkillID
from src.constant.enum.skill_modified_info import SkillModifiedInfo
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillTao(CommandSkill):

    def __init__(self, caster_id: int, args: list) -> None:
        super().__init__(caster_id, args)
        if len(args) != 0:
            pos = 0
            self.targets = []
            self.times = []
            while pos + 1 < len(args):
                self.targets.append(args[pos])
                self.times.append(args[1 + pos])
                pos += 2
        else:
            # 参数留空时，默认对自己使用
            self.targets = [self.caster_id]
            self.times = [1]

    def __str__(self) -> str:
        s = ""
        for idx in range(len(self.targets)):
            s += f"{self.targets[idx]}({self.times[idx]} Times)  "
        return f"{self.caster_id} -{self.GetTitle()}> {s}"

    @staticmethod
    def NewSkill(
        caster, args: list[str], game: "Game|None" = None
    ) -> tuple[bool, Skill | None, str]:
        if len(args) == 0:
            return True, SkillTao(caster, []), ""
        elif len(args) % 2 != 0:
            return False, None, "桃参数需要为偶数"
        else:
            ret = []
            for arg in args:
                try:
                    iarg = int(arg)
                except ValueError:
                    iarg = -1

                if iarg < 0:
                    return False, None, f"参数错误{arg}"
                ret.append(iarg)

            return True, SkillTao(caster, ret), ""

    def GetAllTimes(self) -> int:
        """获得使用技能的所有次数"""
        return sum(self.times)

    def GetTargetTimes(self, target_id: int) -> int:
        """对目标使用了多少次技能"""
        try:
            idx = self.targets.index(target_id)
        except ValueError:
            idx = -1

        if idx < 0:
            return 0
        return self.times[idx]

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "桃"

    @staticmethod
    def GetName() -> str:
        return "tao"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """指定目标，使目标+1，且目标可以为包括自己的所有人，同一回合可以使用多个桃，且可以分配"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 3

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetAllTimes() * self.GetBasicPoint()

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.COMMAND

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.TAO

    @staticmethod
    def GetCmdOccasion() -> int:
        return 1

    def SetTarget(self, new_target: list[int]):
        """用于trigger修改原技能的target"""
        self.targets = new_target

    def IsValidToTarget(self, target_id: int) -> bool:
        _ = self.ParseItemModifiedInfo(self.modified_info, SkillModifiedInfo.INVALIDATED)
        if (self.caster_id, target_id) in _:
            return False
        else:
            return True

    # 使用类
    def Cast(self, game: "Game"):
        # print(self.targets)
        """在结算时候的释放技能"""
        for idx in range(len(self.targets)):
            target_id = self.targets[idx]
            times = self.times[idx]

            if not self.IsValidToTarget(target_id):
                continue

            if game.Skill_Used_Times.get(SkillID.XIADU, 0) != 0:
                game.players[target_id].ChangeHealth(
                    game.Skill_Used_Times[SkillID.XIADU] * times * (-3),
                    game
                )
            else:
                game.players[target_id].ChangeHealth(times * 1, game)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillTao.GetSkillID().value] = SkillTao
Skill_Name_To_ID[SkillTao.GetName()] = SkillTao.GetSkillID().value
