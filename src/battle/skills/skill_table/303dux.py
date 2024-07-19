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

class SkillDuX(CommandSkill):

    def __init__(self, caster_id: int, args: list, game: "Game|None" = None) -> None:
        super().__init__(caster_id, args)
        self.x = int(args[0])
        self.game = game

    def __str__(self) -> str:
        return f"{self.caster_id} -> {self.GetTitle()[:-1]}{self.x}"

    @staticmethod
    def NewSkill(
        caster, args: list[str], game: "Game|None" = None
    ) -> tuple[bool, Skill | None, str]:
        if len(args) != 1:
            return False, None, "赌X参数需为1"
        if int(args[0]) <= 0:
            return False, None, "赌X参数需大于0" # 先不考虑负数档，可以之后再补充
        else:
            return True, SkillDuX(caster, args, game), ""

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "赌X"

    @staticmethod
    def GetName() -> str:
        return "dux"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """若你本回合有血量变动的人数等于x，则你恢复至初始血量。当场上只有两人时，赌1变为3点。"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 1

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        if len(self.game.GetLiveUIDs())>= 2:
            return self.GetBasicPoint()
        else:
            return 3

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.COMMAND

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.DUX

    @staticmethod
    def GetCmdOccasion() -> int:
        return 4
        
    # 使用类
    def Cast(self, game: "Game"):
        """在结算时候的释放技能"""
        if len(game.GetHurtPlayers()) + game.Skill_Used_Times.get(SkillID.XIADU,0) == self.x:
            game.players[self.caster_id].ResetHealth()



from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillDuX.GetSkillID().value] = SkillDuX
Skill_Name_To_ID[SkillDuX.GetName()] = SkillDuX.GetSkillID().value
