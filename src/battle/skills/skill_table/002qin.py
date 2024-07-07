from src.models.battle.skill import Skill
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillQin(Skill):
    def __init__(self) -> None:
        super().__init__()

    def GetName(self) -> str:
        """获取技能名称"""
        return "揿(qin)"

    def GetDescription(self) -> str:
        """获取技能描述"""
        return """目标-3，若p杀遇q揿，杀方+pq，揿方-pq"""

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return 1

    def GetSkillType(self) -> SkillType:
        return SkillType.SINGLE

    def GetSkillID(self) -> SkillID:
        return SkillID.QIN

    # 使用类

    def JudgeLegal(self, target_id: int, times: int, game: "Game") -> bool:
        """检测技能是否参数正确"""
        return True

    def Cast(self, caster_id: int, target_id: int, times: int, game: "Game"):
        """在结算时候的释放技能"""
        # 针对防御等级
        if game.players[target_id].defense_level >= 1:  # "防御"
            return  # 无效化

        # 针对sha
        is_used, used_times = game.Skill_Stash.IsPlayerUseSpecifiedSkillToPlayer(
            target_id, caster_id, SkillID.SHA
        )
        if is_used:
            # game.players[caster_id].ChangeHealth(-times * used_times * 1) 已经在杀的地方计算过了
            game.players[target_id].ChangeHealth(+times * used_times * 1)
            return

        # 针对法攻
        is_used, used_times = game.Skill_Stash.IsPlayerUseSpecifiedSkillToPlayer(
            target_id, caster_id, SkillID.FAGONG
        )
        if is_used:
            return  # 遇到法攻无效

        game.players[target_id].ChangeHealth(-times * 3)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

__skill = SkillQin()
Skill_Table[__skill.GetSkillID().value] = __skill
Skill_Name_To_ID[__skill.GetName()] = __skill.GetSkillID().value
