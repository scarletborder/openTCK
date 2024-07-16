# from src.models.battle.game import Game
from src.models.battle.skill import CommandSkill, Skill
from src.constant.enum.skill import SkillType, SkillID
from src.constant.enum.skill_modified_info import SkillModifiedInfo
from src.constant.enum.battle_trigger import TriggerType
from src.models.battle.trigger import SpecifiedPlayerTrigger
from src.constant.enum.battle_tag import TagEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class JiuTrigger(SpecifiedPlayerTrigger):
    def __init__(self, game: "Game", tri_type: TriggerType, sk: Skill, sp_plid: int):
        super().__init__(game, tri_type, sk, sp_plid)

    @staticmethod
    def NewTrigger(game: "Game", sk: Skill, arg: int) -> SpecifiedPlayerTrigger:
        """param arg: target_id"""
        tri = JiuTrigger(game, TriggerType.B_SPECIFIEDPLAYER, sk, arg)
        return tri

    def Cast(self, game: "Game", sk: Skill):
        if sk.GetSkillID == SkillID.SHA or sk.GetSkillID == SkillID.QIN:
            sk.SetModifiedInfo(SkillModifiedInfo.EXTRA_DAMAGE, 1)


class SkillJiu(CommandSkill):

    def __init__(self, caster_id: int, args: list) -> None:
        super().__init__(caster_id, args)

    @staticmethod
    def NewSkill(
        caster, args: list[str], game: "Game|None" = None
    ) -> tuple[bool, Skill | None, str]:
        if len(args) == 0:
            return True, SkillJiu(caster, []), ""
        else:
            return False, None, "酒不需要别的参数"

    def GetAllTimes(self) -> int:
        """获得使用技能的所有次数"""
        return 1

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "酒"

    @staticmethod
    def GetName() -> str:
        return "jiu"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """清空自身“腐化”标记。若自身处于濒死，则+1；若不是，则下一回合“杀”和“揿”的伤害+1."""

    @staticmethod
    def GetBasicPoint() -> int:
        return 1

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetAllTimes() * self.GetBasicPoint()

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.COMMAND

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.JIU

    @staticmethod
    def GetCmdOccasion() -> int:
        return 1

    # 使用类
    def Cast(self, game: "Game"):
        """在结算时候的释放技能"""
        game.players[self.caster_id].tag[TagEvent.FUHUA] = 0
        if game.Skill_Used_Times.get(SkillID.XIADU, 0) != 0:
            game.players[self.caster_id].ChangeHealth(
                game.Skill_Used_Times[SkillID.XIADU] * (-3)
            )
        elif game.players[self.caster_id].Health == 0:
            game.players[self.caster_id].ChangeHealth(1)

        tri = JiuTrigger.NewTrigger(game, self, self.caster_id)
        game.AddNextTrigger(tri)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillJiu.GetSkillID().value] = SkillJiu
Skill_Name_To_ID[SkillJiu.GetName()] = SkillJiu.GetSkillID().value
