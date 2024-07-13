from src.models.battle.skill import Skill, SingleAttackSkill
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillFagong(SingleAttackSkill):

    def __init__(self, caster_id: int, args: list) -> None:
        """args为偶数个，[0]为目标，[1]为次数"""
        super().__init__(caster_id, args)

    @staticmethod
    def NewSkill(caster, args: list[str]) -> tuple[bool, Skill | None, str]:
        if len(args) % 2 != 0:
            return False, None, "单体攻击参数需要为偶数"
        ret = []
        for arg in args:
            try:
                iarg = int(arg)
            except ValueError:
                iarg = -1

            if iarg < 0:
                return False, None, f"参数错误{arg}"

            ret.append(iarg)

        return True, SkillFagong(caster, ret), ""

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "法攻"

    @staticmethod
    def GetName() -> str:
        return "fagong"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """目标-1，若遇杀，则法攻无效；若遇揿，则双方均无效"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 2

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetAllTimes() * self.GetBasicPoint()

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.SINGLE

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.FAGONG

    @staticmethod
    def GetAttackLevel() -> int:
        return 2

    # 使用类

    def JudgeLegal(self, target_id: int, times: int, game: "Game") -> bool:
        """检测技能是否参数正确"""
        return True

    def Cast(self, caster_id: int, target_id: int, times: int, game: "Game"):
        """在结算时候的释放技能"""
        for idx in range(len(self.targets)):
            target_id = self.targets[idx]
            times = self.times[idx]
            # 针对防御等级
            if game.players[target_id].defense_level >= 2:  # "高防"
                return  # 无效化

            # 针对sha
            is_used, sk = game.Skill_Stash.IsPlayerUseSpecifiedSkill(
                target_id, SkillID.SHA
            )
            if is_used and sk and sk.GetTargetTimes(target_id) > 0:
                continue  # 遇到杀无效

            # 针对qin
            is_used, sk = game.Skill_Stash.IsPlayerUseSpecifiedSkill(
                target_id, SkillID.QIN
            )
            if is_used and sk and sk.GetTargetTimes(target_id) > 0:
                continue  # 遇到qin双方无效

            game.players[target_id].ChangeHealth(-times * 1)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillFagong.GetSkillID().value] = SkillFagong
Skill_Name_To_ID[SkillFagong.GetName()] = SkillFagong.GetSkillID().value
