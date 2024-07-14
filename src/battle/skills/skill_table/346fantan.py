from src.constant.enum.battle_trigger import TriggerType
from src.models.battle.game import Game
from src.models.battle.skill import CommandSkill, Skill, AttackSkill
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

from src.models.battle.trigger import BattleTrigger
from src.models.battle.trigger import SpecifiedSkillTrigger, SpecifiedPlayerTrigger

if TYPE_CHECKING:
    from src.models.battle.game import Game, TriggerType


class FantanTaoTrigger(SpecifiedPlayerTrigger):
    def __init__(
        self, game: "Game", tri_type: TriggerType, sk: Skill, sp_plid: int
    ):
        super().__init__(game, tri_type, sk, sp_plid)

    @staticmethod
    def NewTrigger(game: "Game", sk: Skill, arg: int) -> SpecifiedPlayerTrigger:
        """param arg: target_id"""
        tri = FantanTaoTrigger(game, TriggerType.B_SPECIFIEDPLAYER, sk, arg)
        return tri

    def Cast(self, game: "Game", sk: Skill):
        """
        param game: 游戏
        type game: Game
        param sk: 需要修改的技能
        type sk: AttackSkill
        """
        target_targets = sk.targets
        if self.Original_Skill.caster_id in target_targets:
            target_targets = [sk.caster_id if i == self.Original_Skill.caster_id else i for i in target_targets] # 将目标修改为自身
        sk.SetTarget(target_targets)
        
class FantanAttackTrigger(SpecifiedPlayerTrigger):
    def __init__(
        self, game: "Game", tri_type: TriggerType, sk: Skill, sp_plid: int
    ):
        super().__init__(game, tri_type, sk, sp_plid)

    @staticmethod
    def NewTrigger(game: "Game", sk: Skill, arg: int) -> SpecifiedPlayerTrigger:
        """@arg: target_id"""
        if isinstance(sk, AttackSkill):
            tri = FantanAttackTrigger(game, TriggerType.B_SPECIFIEDPLAYER, sk, arg)
        else:
            return None
        return tri
    
    def Cast(self, game: "Game", sk: AttackSkill):
        """
        param game: 游戏
        type game: Game
        param sk: 需要修改的技能
        type sk: AttackSkill
        """
        target_targets = sk.targets
        if self.Original_Skill.caster_id in target_targets:
            target_targets = [sk.caster_id if i == self.Original_Skill.caster_id else i for i in target_targets] # 将目标修改为自身
        sk.SetTarget(target_targets)

class SkillFantan(CommandSkill):

    def __init__(self, caster_id: int, args: list, game: "Game|None" = None) -> None:
        super().__init__(caster_id, args)
        self.target = args[0]
        self.game = game

    def __str__(self) -> str:
        return f"{self.caster_id} -> {self.GetTitle()} ({self.GetAllTimes()} Times)"

    @staticmethod
    def NewSkill(caster, args: list[str], game: "Game|None" = None) -> tuple[bool, Skill | None, str]:
        if len(args) != 1:
            return False, None, "反弹参数需为1"
        elif game.players[caster].Point <= 0:
            return False, None, "你没有点数"
        else:
            return True, SkillFantan(caster, []), ""

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
    def GetBasicPoint(self) -> int:
        return self.game.players[self.caster_id].Point

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetBasicPoint()

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
        tri_attack = FantanAttackTrigger.NewTrigger(game, self, self.GetAllTimes())
        game.AddTrigger(tri_attack)
        tri_tao = FantanTaoTrigger.NewTrigger(game, self, self.GetAllTimes())
        game.AddTrigger(tri_tao)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillFantan.GetSkillID().value] = SkillFantan
Skill_Name_To_ID[SkillFantan.GetName()] = SkillFantan.GetSkillID().value
