from src.constant.enum.battle_trigger import TriggerType
from src.models.battle.skill import CommandSkill, Skill, AttackSkill
from src.constant.enum.skill_modified_info import SkillModifiedInfo
from src.constant.enum.battle_tag import TagEvent
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game, TriggerType


class SkillHudun(CommandSkill):

    def __init__(self, caster_id: int, args: list) -> None:
        super().__init__(caster_id, args)
        self.times = [1]

    @staticmethod
    def NewSkill(
        caster, args: list[str], game: "Game|None" = None
    ) -> tuple[bool, Skill | None, str]:
        if len(args) == 0:
            return True, SkillHudun(caster, []), ""
        else:
            return False, None, "护盾不需要参数"

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "护盾"

    @staticmethod
    def GetName() -> str:
        return "hudun"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """本回合自身获得一个“护盾”标记。当拥有“护盾”标记的玩家受到伤害时，消耗一个“护盾”标记，并抵挡这一回合的任意伤害"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 5

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetBasicPoint()

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.COMMAND

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.HUDUN

    @staticmethod
    def GetCmdOccasion() -> int:
        return 1

    # 使用类
    def Cast(self, game: "Game"):
        game.players[self.caster_id].tag[TagEvent.HUDUN] = (
            game.players[self.caster_id].tag.get(TagEvent.HUDUN, 0) + 1 * self.times[0]
        )


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillHudun.GetSkillID().value] = SkillHudun
Skill_Name_To_ID[SkillHudun.GetName()] = SkillHudun.GetSkillID().value
