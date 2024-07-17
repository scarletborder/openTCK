from src.constant.enum.battle_trigger import TriggerType
from src.models.battle.skill import CommandSkill, Skill, AttackSkill
from src.constant.enum.skill_modified_info import SkillModifiedInfo
from src.constant.enum.battle_tag import TagEvent
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game, TriggerType

class SkillShandian(CommandSkill):

    def __init__(self, caster_id: int, args: list) -> None:
        super().__init__(caster_id, args)

    @staticmethod
    def NewSkill(
        caster, args: list[str], game: "Game|None" = None
    ) -> tuple[bool, Skill | None, str]:
        if len(args) == 0:
            return True, SkillShandian(caster, []), ""
        else:
            return False, None, "闪电不需要参数"

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "闪电"

    @staticmethod
    def GetName() -> str:
        return "shandian"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """本回合自身获得一个“闪电”标记。下一个轮次时，逆时针旋转目标。当场同时出现三个及以上下毒时，“闪电”标记被消耗，且该玩家直接死亡"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 3

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetBasicPoint()

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.COMMAND

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.SHANDIAN

    @staticmethod
    def GetCmdOccasion() -> int:
        return 1

    # 使用类
    def Cast(self, game: "Game"):
        game.players[self.caster_id].tag[TagEvent.SHANDIAN] = 1

from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillShandian.GetSkillID().value] = SkillShandian
Skill_Name_To_ID[SkillShandian.GetName()] = SkillShandian.GetSkillID().value
