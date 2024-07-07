from src.models.battle.skill import Skill
from src.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillFangyu(Skill):
    def __init__(self) -> None:
        super().__init__()

    def GetName(self) -> str:
        """获取技能名称"""
        return "防御"

    def GetDescription(self) -> str:
        """获取技能描述"""
        return """抵挡杀、揿、万箭、吸血"""

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return 0

    def GetSkillType(self) -> SkillType:
        return SkillType.DEFENSE

    def GetSkillID(self) -> SkillID:
        return SkillID.GAOFANG

    # 使用类

    def JudgeLegal(self, target_id: int, times: int, game: "Game") -> bool:
        """检测技能是否参数正确"""
        return True

    def Cast(self, caster_id: int, target_id: int, times: int, game: "Game"):
        """在结算时候的释放技能"""
        # 提升防御等级
        game.players[caster_id].defense_level = 2


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

__skill = SkillFangyu()
Skill_Table[__skill.GetSkillID().value] = __skill
Skill_Name_To_ID[__skill.GetName()] = __skill.GetSkillID().value
