from src.constant.enum.battle_trigger import TriggerType
from src.models.battle.game import Game
from src.models.battle.skill import CommandSkill, Skill
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

from src.models.battle.trigger import BattleTrigger
from src.models.battle.trigger import SpecifiedSkillTrigger

if TYPE_CHECKING:
    from src.models.battle.game import Game, TriggerType


class TaoTrigger(SpecifiedSkillTrigger):
    def __init__(
        self, game: "Game", tri_type: TriggerType, sk: Skill, sp_skid: SkillID
    ):
        super().__init__(game, tri_type, sk, sp_skid)

    @staticmethod
    def NewTrigger(game: "Game", sk: Skill, arg: int) -> BattleTrigger:
        """@arg: 几份毒"""
        tri = TaoTrigger(game, TriggerType.B_SPECIFIEDSKILL, sk, SkillID.TAO)

        return tri

    def Cast(self, game: "Game", arg: Skill):
        """对使用桃的目标，在生效前篡改其cast函数"""
        original_skill = self.Original_Skill

        def Cast(self, game: "Game"):
            nonlocal original_skill

            for idx in range(len(self.targets)):
                target_id = self.targets[idx]
                times = self.times[idx]

                game.players[target_id].ChangeHealth(
                    -times * original_skill.GetAllTimes() * 3, game, original_skill
                )

        arg.SetCast(Cast)


class SkillXiadu(CommandSkill):

    def __init__(self, caster_id: int, args: list) -> None:
        super().__init__(caster_id, args)
        if len(args) == 1:
            self.times = args[0]  # 毒的次数
        elif len(args) == 0:
            # 参数留空时，默认下一份毒
            self.times = 1

    def __str__(self) -> str:
        return f"{self.caster_id} -> {self.GetTitle()} ({self.GetAllTimes()} Times)"

    @staticmethod
    def NewSkill(caster, args: list[str]) -> tuple[bool, Skill | None, str]:
        if len(args) >= 2:
            return False, None, "下毒参数至多为1"
        elif len(args) == 0:
            return True, SkillXiadu(caster, []), ""
        else:
            ret = []
            for arg in args:
                try:
                    iarg = int(arg)
                except ValueError:
                    iarg = -1

                if iarg < 0:
                    return False, None, f"参数错误{arg}"
                ret.append(iarg)

            return True, SkillXiadu(caster, ret), ""

    def GetAllTimes(self) -> int:
        """获得使用技能的所有次数"""
        return self.times

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "下毒"

    @staticmethod
    def GetName() -> str:
        return "xiadu"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """同一回合可以使用多个下毒。若场上有玩家使用桃和酒，各个玩家受到按照各自的桃、
酒的数量乘场上的下毒数的伤害。并且拥有防住火舞的能力。其他效果见“赌x”“0档”“闪电”条目"""

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
        return SkillID.XIADU

    @staticmethod
    def GetCmdOccasion() -> int:
        return 1

    # 使用类
    def Cast(self, game: "Game"):
        """在结算时候的释放技能"""
        # 添加trigger
        tri = TaoTrigger.NewTrigger(game, self, self.GetAllTimes())
        game.AddTrigger(tri)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillXiadu.GetSkillID().value] = SkillXiadu
Skill_Name_To_ID[SkillXiadu.GetName()] = SkillXiadu.GetSkillID().value
