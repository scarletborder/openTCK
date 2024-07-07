from src.models.battle.skill import Skill
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillGaofang(Skill):
    def __init__(self) -> None:
        super().__init__()

    def GetName(self) -> str:
        """获取技能名称"""
        return "法攻"

    def GetDescription(self) -> str:
        """获取技能描述"""
        return """抵挡法攻、吸血、冰冻、腐化、万箭、南蛮、雷电、火舞"""

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return 2

    def GetSkillType(self) -> SkillType:
        return SkillType.DEFENSE

    def GetSkillID(self) -> SkillID:
        return SkillID.FANGYU

    # 使用类

    def JudgeLegal(self, target_id: int, times: int, game: "Game") -> bool:
        """检测技能是否参数正确"""
        return True

    def Cast(self, caster_id: int, target_id: int, times: int, game: "Game"):
        """在结算时候的释放技能"""
        # 提升防御等级
        game.players[caster_id].defense_level = 1


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

__skill = SkillGaofang()
Skill_Table[__skill.GetSkillID().value] = __skill
Skill_Name_To_ID[__skill.GetName()] = __skill.GetSkillID().value
