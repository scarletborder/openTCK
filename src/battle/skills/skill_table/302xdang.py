from src.constant.enum.battle_trigger import TriggerType

# from src.models.battle.game import Game
from src.models.battle.skill import CommandSkill, Skill, AttackSkill
from src.constant.enum.skill import SkillType, SkillID
from src.constant.enum.skill_modified_info import SkillModifiedInfo
from typing import TYPE_CHECKING

from src.models.battle.trigger import BattleTrigger
from src.models.battle.trigger import SpecifiedTargetTrigger, SpecifiedPlayerTrigger

if TYPE_CHECKING:
    from src.models.battle.game import Game, TriggerType

class SkillXDang(CommandSkill):

    def __init__(self, caster_id: int, args: list, game: "Game|None" = None) -> None:
        super().__init__(caster_id, args)
        self.x = int(args[0])
        self.game = game

    def __str__(self) -> str:
        return f"{self.caster_id} -> {self.x}{self.GetTitle()[1:]}"

    @staticmethod
    def NewSkill(
        caster, args: list[str], game: "Game|None" = None
    ) -> tuple[bool, Skill | None, str]:
        if len(args) != 1:
            return False, None, "X档参数需为1"
        if int(args[0]) <= 0:
            return False, None, "X档参数需大于0" # 先不考虑负数档，可以之后再补充
        else:
            return True, SkillXDang(caster, args, game), ""

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "X档"

    @staticmethod
    def GetName() -> str:
        return "xdang"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """若你本回合的血量变动等于x，则你恢复至初始血量"""

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
        return SkillID.XDANG

    @staticmethod
    def GetCmdOccasion() -> int:
        return 4
        
    # 使用类
    def Cast(self, game: "Game"):
        """在结算时候的释放技能"""
        if game.players[self.caster_id].health_change == -self.x:
            game.players[self.caster_id].ResetHealth()



from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillXDang.GetSkillID().value] = SkillXDang
Skill_Name_To_ID[SkillXDang.GetName()] = SkillXDang.GetSkillID().value
