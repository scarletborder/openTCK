from src.models.battle.skill import Skill
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillJidian(Skill):

    def __init__(self, caster_id: int, args: list) -> None:
        """无args"""
        super().__init__(caster_id, args)
        return

    @staticmethod
    def NewSkill(caster, args: list[str]) -> tuple[bool, Skill | None, str]:
        if len(args) > 0:
            return False, None, "积点不接受参数"

        return True, SkillJidian(caster, []), ""

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "积点"

    @staticmethod
    def GetName() -> str:
        return "jidian"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """使玩家获得一个点数"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 0

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetBasicPoint()

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.COMMAND

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.JIDIAN

    # 使用类

    def JudgeLegal(self, target_id: int, times: int, game: "Game") -> bool:
        """检测技能是否参数正确"""
        return True

    def Cast(self, game: "Game"):
        """在结算时候的释放技能"""
        # +1point
        game.players[self.caster_id].ChangePoint(+1)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillJidian.GetSkillID().value] = SkillJidian
Skill_Name_To_ID[SkillJidian.GetName()] = SkillJidian.GetSkillID().value
