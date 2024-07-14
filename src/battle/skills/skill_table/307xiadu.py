from src.models.battle.skill import CommandSkill, Skill
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillTao(CommandSkill):

    def __init__(self, caster_id: int, args: list) -> None:
        super().__init__(caster_id, args)
        if len(args) != 0:
            pos = 0
            self.targets = []
            self.times = []
            while pos + 1 < len(args):
                self.targets.append(args[pos])
                self.times.append(args[1 + pos])
                pos += 2
        else:
            # 参数留空时，默认对自己使用
            self.targets = [self.caster_id]
            self.times = [1]

    def __str__(self) -> str:
        s = ""
        for idx in range(len(self.targets)):
            s += f"{self.targets[idx]}({self.times[idx]} Times)  "
        return f"{self.caster_id} -{self.GetTitle()}> {s}"

    @staticmethod
    def NewSkill(caster, args: list[str]) -> tuple[bool, Skill | None, str]:
        if len(args) == 0:
            return False, None, "请至少选择一名玩家进行下毒"
        elif len(args) % 2 != 0:
            return False, None, "下毒参数需要为偶数"
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

            return True, SkillTao(caster, ret), ""

    def GetAllTimes(self) -> int:
        """获得使用技能的所有次数"""
        return sum(self.times)

    def GetTargetTimes(self, target_id: int) -> int:
        """对目标使用了多少次技能"""
        try:
            idx = self.targets.index(target_id)
        except ValueError:
            idx = -1

        if idx < 0:
            return 0
        return self.times[idx]

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
        for idx in range(len(self.targets)):
            target_id = self.targets[idx]
            times = self.times[idx]

            game.players[target_id].ChangeHealth(+times * 1)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillTao.GetSkillID().value] = SkillTao
Skill_Name_To_ID[SkillTao.GetName()] = SkillTao.GetSkillID().value
