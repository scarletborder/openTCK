from src.models.battle.skill import Skill, SingleAttackSkill
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillQin(SingleAttackSkill):
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

        return True, SkillQin(caster, ret), ""

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "揿(qin)"

    @staticmethod
    def GetName() -> str:
        return "qin"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """[lev 1]目标-3，若p杀遇q揿，杀方+pq，揿方-pq"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 1

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetAllTimes() * self.GetBasicPoint()

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.SINGLE

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.QIN

    @staticmethod
    def GetAttackLevel() -> int:
        return 1

    # 使用类

    def JudgeLegal(self, target_id: int, times: int, game: "Game") -> bool:
        """检测技能是否参数正确"""
        return True

    def Cast(self, game: "Game"):
        """在结算时候的释放技能"""
        for idx in range(len(self.targets)):
            target_id = self.targets[idx]
            times = self.times[idx]
            # 针对防御等级
            if game.players[target_id].defense_level >= 1:  # "防御"
                return  # 无效化

            # 针对sha
            is_used, sk = game.Skill_Stash.IsPlayerUseSpecifiedSkill(
                target_id, SkillID.SHA
            )

            if is_used and sk:
                used_times = sk.GetTargetTimes(self.caster_id)
                if used_times > 0:
                    # 自己掉血
                    game.players[self.caster_id].ChangeHealth(-times * used_times * 1)
                    # 给杀方回血
                    game.players[target_id].ChangeHealth(+times * used_times * 1)  # type: ignore
                    continue

            # 针对法攻
            is_used, sk = game.Skill_Stash.IsPlayerUseSpecifiedSkill(
                target_id, SkillID.FAGONG
            )
            if is_used and sk and sk.GetTargetTimes(self.caster_id) > 0:
                continue  # 遇到法攻无效

            game.players[target_id].ChangeHealth(-times * 3)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillQin.GetSkillID().value] = SkillQin
Skill_Name_To_ID[SkillQin.GetName()] = SkillQin.GetSkillID().value
