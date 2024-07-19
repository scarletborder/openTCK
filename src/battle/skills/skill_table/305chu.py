from src.constant.enum.battle_trigger import TriggerType
from src.models.battle.skill import CommandSkill, Skill
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

from src.models.battle.trigger import BattleTrigger
from src.models.battle.trigger import SpecifiedSkillTrigger

if TYPE_CHECKING:
    from src.models.battle.game import Game, TriggerType


class ChuTrigger(SpecifiedSkillTrigger):
    @staticmethod
    def NewTrigger(game: "Game", sk: Skill, sp_skid: SkillID) -> SpecifiedSkillTrigger:
        tri = ChuTrigger(game, TriggerType.B_SPECIFIEDSKILL, sk, sp_skid)
        return tri

    def Cast(self, game: "Game", sk: Skill):

        # 直接修改相应技能的Cast函数为空，这是有风险的写法

        def Cast(self, game: "Game", sk: Skill):
            return

        sk.SetCast(Cast)


class SkillChu(CommandSkill):

    def __init__(self, caster_id: int, args: list) -> None:
        super().__init__(caster_id, args)

    @staticmethod
    def NewSkill(
        caster, args: list[str], game: "Game|None" = None
    ) -> tuple[bool, Skill | None, str]:
        if len(args) == 0:
            return True, SkillChu(caster, []), ""
        else:
            return False, None, "除不需要参数"

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "除"

    @staticmethod
    def GetName() -> str:
        return "chu"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """使全场X档、赌X、X倍无效"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 1

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetBasicPoint()

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.COMMAND

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.CHU

    @staticmethod
    def GetCmdOccasion() -> int:
        return 1

    # 使用类
    def Cast(self, game: "Game"):
        for sp_skid in [SkillID.XDANG, SkillID.DUX]:
            tri = ChuTrigger.NewTrigger(game, self, sp_skid)
            game.AddTrigger(tri)

from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillChu.GetSkillID().value] = SkillChu
Skill_Name_To_ID[SkillChu.GetName()] = SkillChu.GetSkillID().value
