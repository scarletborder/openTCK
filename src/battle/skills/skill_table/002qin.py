from src.models.battle.skill import *
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
    def Cast(self, game: "Game"):
        """在结算时候的释放技能"""
        caster_id = self.caster_id
        for idx in range(len(self.targets)):
            target_id = self.targets[idx]
            times = self.times[idx]
            target_skill, target_targets = game.Skill_Stash.GetTargetSkill(target_id)
            if isinstance(target_skill, AttackSkill):
                if caster_id in target_targets:
                    if target_skill.GetSkillID() == SkillID.SHA: # p Qin遇q Sha,揿方-pq,杀方+pq
                        used_times = target_skill.GetTargetTimes(self.caster_id)
                        game.players[self.caster_id].ChangeHealth(-times * used_times * 1)
                        game.players[target_id].ChangeHealth(+times * used_times * 1)  # type: ignore
                        continue
                    elif target_skill.GetAttackLevel() >= self.GetAttackLevel(): # 遇到高级攻击无效
                        continue
            elif isinstance(target_skill, DefenseSkill):
                # 针对防御等级
                if game.players[target_id].defense_level >= 1 and game.players[target_id].defense_level != 2:  # "Gaofang"无法防御，其他则可以
                    continue  # 无效化           
            elif isinstance(target_skill, CommandSkill):
                pass
            game.players[target_id].ChangeHealth(-times * 3)

from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillQin.GetSkillID().value] = SkillQin
Skill_Name_To_ID[SkillQin.GetName()] = SkillQin.GetSkillID().value
