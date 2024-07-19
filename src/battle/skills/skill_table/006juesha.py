from src.models.battle.skill import *
from src.constant.enum.skill import SkillType, SkillID
from src.constant.enum.skill_modified_info import SkillModifiedInfo
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillSha(SingleAttackSkill):
    def __init__(self, caster_id: int, args: list) -> None:
        super().__init__(caster_id, args)

    @staticmethod
    def NewSkill(caster, args: list[str], game: "Game|None" = None) -> tuple[bool, Skill | None, str]:
        if len(args) == 0:
            return False, None, "请至少选择一名玩家进行攻击"
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
        return "绝杀"

    @staticmethod
    def GetName() -> str:
        return "juesha"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """目标-1，且无视攻击等级、防御等级和反弹"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 3

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetAllTimes() * self.GetBasicPoint()
    
    def GetDamage(self) -> int:
        """获取技能最终伤害"""
        damage = 1
        for extra_damage in Skill.ParseItemModifiedInfo(self.modified_info, SkillModifiedInfo.EXTRA_DAMAGE):
            damage += int(extra_damage)
        return damage

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.SINGLE

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.JUESHA

    @staticmethod
    def GetAttackLevel() -> int:
        return 3

    # 使用类
    def Cast(self, game: "Game"):
        caster_id = self.caster_id
        for idx in range(len(self.targets)):
            target_id = self.targets[idx]
            times = self.times[idx]
            target_skill, target_targets = game.Skill_Stash.GetTargetSkillDetail(
                target_id
            )

            if not self.IsValidToTarget(target_id):
                continue
            
            elif isinstance(target_skill, AttackSkill):
                pass
            elif isinstance(target_skill, DefenseSkill):
                pass
            elif isinstance(target_skill, CommandSkill):
                pass

            game.players[target_id].ChangeHealth(-times * self.GetDamage())


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402


Skill_Table[SkillSha.GetSkillID().value] = SkillSha
Skill_Name_To_ID[SkillSha.GetName()] = SkillSha.GetSkillID().value
