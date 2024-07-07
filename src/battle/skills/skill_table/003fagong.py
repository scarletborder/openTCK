from src.models.battle.skill import Skill
from src.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillFagong(Skill):
    def __init__(self) -> None:
        super().__init__()

    def GetName(self) -> str:
        """获取技能名称"""
        return "法攻"

    def GetDescription(self) -> str:
        """获取技能描述"""
        return """目标-1，若遇杀，则法攻无效；若遇揿，则双方均无效"""

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return 2

    def GetSkillType(self) -> SkillType:
        return SkillType.SINGLE

    def GetSkillID(self) -> SkillID:
        return SkillID.FAGONG

    # 使用类

    def JudgeLegal(self, target_id: int, times: int, game: "Game") -> bool:
        """检测技能是否参数正确"""
        return True

    def Cast(self, caster_id: int, target_id: int, times: int, game: "Game"):
        """在结算时候的释放技能"""
        # 针对防御等级
        if game.players[target_id].defense_level >= 2:  # "高防"
            return  # 无效化

        # 针对sha
        is_used, used_times = game.Skill_Stash.IsPlayerUseSpecifiedSkillToPlayer(
            target_id, caster_id, SkillID.SHA
        )
        if is_used:
            return  # 遇到杀无效

        # 针对qin
        is_used, used_times = game.Skill_Stash.IsPlayerUseSpecifiedSkillToPlayer(
            target_id, caster_id, SkillID.QIN
        )
        if is_used:
            return  # 遇到qin双方无效

        game.players[target_id].ChangeHealth(-times * 1)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

__skill = SkillFagong()
Skill_Table[__skill.GetSkillID().value] = __skill
Skill_Name_To_ID[__skill.GetName()] = __skill.GetSkillID().value
