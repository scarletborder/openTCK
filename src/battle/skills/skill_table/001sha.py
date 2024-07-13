from src.models.battle.skill import *
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillSha(SingleAttackSkill):
    def __init__(self, caster_id: int, args: list) -> None:
        super().__init__(caster_id, args)

    @staticmethod
    def NewSkill(caster, args: list[str]) -> tuple[bool, Skill | None, str]:
        if len(args) % 2 != 0:
            return False, None, "单体攻击参数需要为偶数"
        ret = []
        for arg in args:
            try:
                iarg = int(arg)
            except ValueError:
                iarg = -1

            if iarg < 0:
                return False, None, f"参数错误{arg}"

            ret.append(iarg)

        return True, SkillSha(caster, ret), ""

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "杀"

    @staticmethod
    def GetName() -> str:
        return "sha"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """[lev 1]目标-1"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 1

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetAllTimes() * self.GetBasicPoint()

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.SINGLE

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.SHA

    @staticmethod
    def GetAttackLevel() -> int:
        return 1

    # 使用类

    def JudgeLegal(self, target_id: int, times: int, game: "Game") -> bool:
        return True

    def Cast(self, game: "Game"):
        caster_id = self.caster_id
        for idx in range(len(self.targets)):
            target_id = self.targets[idx]
            times = self.times[idx]
            target_skill, target_targets = game.Skill_Stash.GetTargetSkill(target_id)
            if isinstance(target_skill, AttackSkill):
                if caster_id in target_targets:
                    if target_skill.GetSkillID() == SkillID.QIN: # qin 单独在qin技能中处理
                        continue
                    elif target_skill.GetAttackLevel() >= 1: # 遇到高级攻击无效
                        if target_skill.GetSkillID() == SkillID.FAGONG: # 遇到法攻则正常
                            game.players[target_id].ChangeHealth(-times * 1)
                            continue
                        else: # 遇到高级攻击无效
                            continue
            elif isinstance(target_skill, DefenseSkill):
                # 针对防御等级
                if game.players[target_id].defense_level >= 1 and game.players[target_id].defense_level != 2:  # "Gaofang"无法防御，其他则可以
                    continue  # 无效化           
            elif isinstance(target_skill, CommandSkill):
                pass
            game.players[target_id].ChangeHealth(-times * 1)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402


Skill_Table[SkillSha.GetSkillID().value] = SkillSha
Skill_Name_To_ID[SkillSha.GetName()] = SkillSha.GetSkillID().value
