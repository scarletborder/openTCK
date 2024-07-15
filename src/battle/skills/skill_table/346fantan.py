from src.constant.enum.battle_trigger import TriggerType
from src.models.battle.game import Game
from src.models.battle.skill import CommandSkill, Skill, AttackSkill
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

from src.models.battle.trigger import BattleTrigger
from src.models.battle.trigger import SpecifiedTargetTrigger, SpecifiedPlayerTrigger

if TYPE_CHECKING:
    from src.models.battle.game import Game, TriggerType


class FantanTrigger(SpecifiedTargetTrigger):
    def __init__(self, game: Game, tri_type: TriggerType, sk: Skill, sp_tid: int, target_id: int):
        super().__init__(game, tri_type, sk, sp_tid)
        self.target_id = target_id

    @staticmethod
    def NewTrigger(game: Game, sk: Skill, arg: int) -> SpecifiedTargetTrigger:
        """param arg: target_id"""
        tri = FantanTrigger(game, TriggerType.B_SPECIFIEDTARGET, sk, sk.caster_id, arg)
        return tri
    
    def Cast(self, game: Game, sk: Skill):
        original_skill = self.Original_Skill
        if (sk.GetSkillID() == SkillID.TAO or isinstance(sk, AttackSkill)):
            sk.SetTarget([int(self.target_id) if i == original_skill.caster_id else i for i in sk.targets])
            
class SkillFantan(CommandSkill):

    def __init__(self, caster_id: int, args: list, game: "Game|None" = None) -> None:
        super().__init__(caster_id, args)
        self.target = args[0]
        self.game = game

    def __str__(self) -> str:
        return f"{self.caster_id} -{self.GetTitle()}> {self.target}"

    @staticmethod
    def NewSkill(caster, args: list[str], game: "Game|None" = None) -> tuple[bool, Skill | None, str]:
        if len(args) != 1:
            return False, None, "反弹参数需为1"
        elif game.players[caster].Point <= 0:
            return False, None, "你没有点数"
        else:
            return True, SkillFantan(caster, args, game), ""

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "反弹"

    @staticmethod
    def GetName() -> str:
        return "fantan"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """反弹攻击技能和桃"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.game.players[self.caster_id].Point

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.COMMAND

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.FANTAN

    @staticmethod
    def GetCmdOccasion() -> int:
        return 1

    # 使用类
    def Cast(self, game: "Game"):
        """在结算时候的释放技能"""
        # 添加trigger
        tri = FantanTrigger.NewTrigger(game, self, self.target)
        game.AddTrigger(tri)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillFantan.GetSkillID().value] = SkillFantan
Skill_Name_To_ID[SkillFantan.GetName()] = SkillFantan.GetSkillID().value
