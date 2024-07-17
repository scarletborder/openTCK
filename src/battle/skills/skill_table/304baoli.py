from src.constant.enum.battle_trigger import TriggerType
from src.models.battle.skill import CommandSkill, Skill
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

from src.models.battle.trigger import BattleTrigger
from src.models.battle.trigger import SpecifiedSkillTrigger

if TYPE_CHECKING:
    from src.models.battle.game import Game, TriggerType


class BaoliTrigger(SpecifiedSkillTrigger):
    @staticmethod
    def NewTrigger(game: "Game", sk: Skill) -> SpecifiedSkillTrigger:
        tri = BaoliTrigger(game, TriggerType.B_SPECIFIEDSKILL, sk, SkillID.BAOLI)
        return tri

    def Cast(self, game: "Game", sk: Skill):

        # 直接修改Fantan的Cast函数为空，这是有风险的写法

        def Cast(self, game: "Game", sk: Skill):
            return

        sk.SetCast(Cast)


class SkillBaoli(CommandSkill):

    def __init__(self, caster_id: int, args: list) -> None:
        super().__init__(caster_id, args)

    @staticmethod
    def NewSkill(
        caster, args: list[str], game: "Game|None" = None
    ) -> tuple[bool, Skill | None, str]:
        if len(args) == 0:
            return True, SkillBaoli(caster, []), ""
        else:
            return False, None, "暴力不需要别的参数"

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "暴力"

    @staticmethod
    def GetName() -> str:
        return "baoli"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """使全场反弹无效"""

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
        return SkillID.BAOLI

    @staticmethod
    def GetCmdOccasion() -> int:
        return 1

    # 使用类
    def Cast(self, game: "Game"):
        tri = BaoliTrigger.NewTrigger(game, self)

    # def Cast(self, game: ""Game""):
    #     for i in range(self.times): # 先使用循环，后期需要更改再将其次数写入trigger中
    #         """在结算时候的释放技能"""
    #         # 添加trigger
    #         tri = XiaduTaoTrigger.NewTrigger(game, self)
    #         game.AddTrigger(tri)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillBaoli.GetSkillID().value] = SkillBaoli
Skill_Name_To_ID[SkillBaoli.GetName()] = SkillBaoli.GetSkillID().value
