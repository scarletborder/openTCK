from src.models.battle.skill import Skill
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillSha(Skill):
    def __init__(self) -> None:
        super().__init__()

    def GetName(self) -> str:
        """获取技能名称"""
        return "杀"

    def GetDescription(self) -> str:
        """获取技能描述"""
        return """目标-1"""

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return 1

    def GetSkillType(self) -> SkillType:
        return SkillType.SINGLE

    def GetSkillID(self) -> SkillID:
        return SkillID.SHA

    # 使用类

    def JudgeLegal(self, target_id: int, times: int, game: "Game") -> bool:
        """检测技能是否参数正确"""
        return True

    def Cast(self, caster_id: int, target_id: int, times: int, game: "Game"):
        """在结算时候的释放技能"""
        # 针对防御等级
        if game.players[target_id].defense_level >= 1:  # "防御"
            return  # 无效化

        game.players[target_id].ChangeHealth(-times * 1)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

__skill = SkillSha()
Skill_Table[__skill.GetSkillID().value] = __skill
Skill_Name_To_ID[__skill.GetName()] = __skill.GetSkillID().value
