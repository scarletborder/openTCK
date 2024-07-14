from src.models.battle.skill import Skill, DefenseSkill
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillGaofang(DefenseSkill):

    def __init__(self, caster_id: int, args: list) -> None:
        """无args"""
        super().__init__(caster_id, args)
        return

    @staticmethod
    def NewSkill(caster, args: list[str]) -> tuple[bool, Skill | None, str]:
        if len(args) > 0:
            return False, None, "防御技能不接受参数"

        return True, SkillGaofang(caster, []), ""

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "高防"

    @staticmethod
    def GetName() -> str:
        return "gaofang"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """抵挡法攻、吸血、冰冻、腐化、万箭、南蛮、雷电、火舞"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 1

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetBasicPoint()

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.DEFENSE

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.GAOFANG

    # 使用类
    def Cast(self, game: "Game"):
        """在结算时候的释放技能"""
        # 提升防御等级
        game.players[self.caster_id].defense_level = 2


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillGaofang.GetSkillID().value] = SkillGaofang
Skill_Name_To_ID[SkillGaofang.GetName()] = SkillGaofang.GetSkillID().value
