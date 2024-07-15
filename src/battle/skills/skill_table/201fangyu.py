from src.models.battle.skill import Skill, DefenseSkill
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillFangyu(DefenseSkill):
    def __init__(self, caster_id: int, args: list) -> None:
        """无args"""
        super().__init__(caster_id, args)
        return

    @staticmethod
    def NewSkill(caster, args: list[str], game: "Game|None" = None) -> tuple[bool, Skill | None, str]:
        if len(args) > 0:
            return False, None, "防御技能不接受参数"

        return True, SkillFangyu(caster, []), ""

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "防御"

    @staticmethod
    def GetName() -> str:
        return "fangyu"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """抵挡杀、揿、万箭、吸血"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 0

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetBasicPoint()

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.DEFENSE

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.FANGYU

    # 使用类
    def Cast(self, game: "Game"):
        # 提升防御等级
        game.players[self.caster_id].defense_level = 1


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillFangyu.GetSkillID().value] = SkillFangyu
Skill_Name_To_ID[SkillFangyu.GetName()] = SkillFangyu.GetSkillID().value
