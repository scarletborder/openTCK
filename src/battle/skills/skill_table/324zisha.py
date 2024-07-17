from src.constant.enum.battle_trigger import TriggerType
from src.models.battle.skill import CommandSkill, Skill, AttackSkill
from src.constant.enum.skill_modified_info import SkillModifiedInfo
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

from src.models.battle.trigger import BattleTrigger
from src.models.battle.trigger import SpecifiedTargetTrigger

if TYPE_CHECKING:
    from src.models.battle.game import Game, TriggerType

class ZishaTrigger(SpecifiedTargetTrigger):
    @staticmethod
    def NewTrigger(game: "Game", sk: Skill) -> SpecifiedTargetTrigger:
        """param arg: target_id"""
        tri = ZishaTrigger(game, TriggerType.B_SPECIFIEDTARGET, sk, sk.caster_id)
        return tri

    def Cast(self, game: "Game", sk: Skill):
        if isinstance(sk, AttackSkill):
            sk.SetModifiedInfo([SkillModifiedInfo.INVALIDATED, (sk.caster_id, self.sp_tid)])

class SkillZisha(CommandSkill):

    def __init__(self, caster_id: int, args: list) -> None:
        super().__init__(caster_id, args)
        self.times = [1]

    @staticmethod
    def NewSkill(
        caster, args: list[str], game: "Game|None" = None
    ) -> tuple[bool, Skill | None, str]:
        if len(args) == 0:
            return True, SkillZisha(caster, []), ""
        else:
            return False, None, "自杀不需要参数"

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "自杀"

    @staticmethod
    def GetName() -> str:
        return "zisha"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """自身-1，本回合所有攻击技能对你无效"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 2

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetBasicPoint()

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.COMMAND

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.ZISHA

    @staticmethod
    def GetCmdOccasion() -> int:
        return 1

    # 使用类
    def Cast(self, game: "Game"):
        game.players[self.caster_id].ChangeHealth(-self.times[0] * 1)
        tri = ZishaTrigger.NewTrigger(game, self)
        game.AddTrigger(tri)

from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillZisha.GetSkillID().value] = SkillZisha
Skill_Name_To_ID[SkillZisha.GetName()] = SkillZisha.GetSkillID().value
