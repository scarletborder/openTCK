from src.models.battle.skill import *
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillNanman(MultiAttackSkill):

    def __init__(self, caster_id: int, args: list) -> None:
        """args为空"""
        super().__init__(caster_id, args)

    @staticmethod
    def NewSkill(caster, args: list[str]) -> tuple[bool, Skill | None, str]:
        if len(args) > 0:
            return False, None, "MULTI不需要任何参数"
        else:
            return True, SkillNanman(caster, []), ""
    
    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "南蛮"

    @staticmethod
    def GetName() -> str:
        return "nanman"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """群体攻击，所有目标-3"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 3

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetBasicPoint() # AOE只需要算一次释放点数

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.MULTI

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.NANMAN

    @staticmethod
    def GetAttackLevel() -> int:
        return 3

    # 使用类
    def Cast(self, game: "Game"):
        """在结算时候的释放技能"""
        caster_id = self.caster_id
        for idx in range(len(self.targets)):
            target_id = self.targets[idx]
            times = self.times[idx]

            target_skill, target_targets = game.Skill_Stash.GetTargetSkill(target_id)
            if isinstance(target_skill, AttackSkill):
                if caster_id in target_targets:
                    if target_skill.GetAttackLevel() >= self.GetAttackLevel(): # 遇到高级攻击无效
                        continue
            elif isinstance(target_skill, DefenseSkill):
                # 针对防御等级
                if game.players[target_id].defense_level >= 2:
                    continue  # 无效化                
            elif isinstance(target_skill, CommandSkill):
                pass
            game.players[target_id].ChangeHealth(-times * 3)

from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillNanman.GetSkillID().value] = SkillNanman
Skill_Name_To_ID[SkillNanman.GetName()] = SkillNanman.GetSkillID().value