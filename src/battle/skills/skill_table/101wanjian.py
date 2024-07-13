from src.models.battle.game import Game
from src.models.battle.skill import *
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillWanjian(MultiAttackSkill):

    def __init__(self, caster_id: int, args: list) -> None:
        """args为空"""
        super().__init__(caster_id, args)

    @staticmethod
    def NewSkill(caster, args: list[str]) -> tuple[bool, Skill | None, str]:
        if len(args) > 0:
            return False, None, "MULTI不需要任何参数"
        else:
            return True, SkillWanjian(caster, []), ""

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "万箭"

    @staticmethod
    def GetName() -> str:
        return "wanjian"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """群体攻击，所有目标-2"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 2

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetBasicPoint()  # AOE只需要算一次释放点数

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.MULTI

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.WANJIAN

    @staticmethod
    def GetAttackLevel() -> int:
        return 2

    # 使用类
    def SingleCast(self, game: Game, caster_id: int, target_id: int, times):
        target_skill, target_targets = game.Skill_Stash.getTargetSkillDetail(target_id)
        if isinstance(target_skill, AttackSkill):
            if caster_id in target_targets:
                if (
                    target_skill.GetAttackLevel() >= self.GetAttackLevel()
                ):  # 遇到高级攻击无效
                    return
        elif isinstance(target_skill, DefenseSkill):
            # 针对防御等级
            if game.players[target_id].defense_level >= 1:
                return  # 无效化
        elif isinstance(target_skill, CommandSkill):
            pass
        game.players[target_id].ChangeHealth(-times * 2)

    def Cast(self, game: "Game"):
        """在结算时候的释放技能"""
        super().Cast(game)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillWanjian.GetSkillID().value] = SkillWanjian
Skill_Name_To_ID[SkillWanjian.GetName()] = SkillWanjian.GetSkillID().value
