from src.models.battle.skill import *
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillXixue(SingleAttackSkill):

    def __init__(self, caster_id: int, args: list) -> None:
        """args为偶数个，[0]为目标，[1]为次数"""
        super().__init__(caster_id, args)

    @staticmethod
    def NewSkill(caster, args: list[str], game: "Game|None" = None) -> tuple[bool, Skill | None, str]:
        if len(args) == 0:
            return False, None, "请至少选择一名玩家进行攻击"
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

        return True, SkillXixue(caster, ret), ""

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "吸血"

    @staticmethod
    def GetName() -> str:
        return "xixue"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """目标-1，自身+1，若遇杀，则吸血无效；若遇揿或法攻，则双方均无效"""

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
        return SkillID.XIXUE

    @staticmethod
    def GetAttackLevel() -> int:
        return 2

    # 使用类
    def Cast(self, game: "Game"):
        """在结算时候的释放技能"""
        caster_id = self.caster_id
        for idx in range(len(self.targets)):
            target_id = self.targets[idx]
            times = self.times[idx]

            target_skill, target_targets = game.Skill_Stash.GetTargetSkillDetail(
                target_id
            )

            if not self.IsValidToTarget(target_id):
                continue

            if target_id == caster_id: # 针对反弹
                game.players[caster_id].ChangeHealth(-1 * times)
                game.players[caster_id].ChangeHealth(1 * times)
                continue
            
            elif isinstance(target_skill, AttackSkill):
                if isinstance(target_skill, SingleAttackSkill):
                    # 是单体攻击
                    if caster_id in target_targets:
                        if target_skill.GetSkillID() == SkillID.SHA:  # 遇到sha无效
                            continue
                        elif target_skill.GetSkillID() == SkillID.QIN:  # 遇到qin无效
                            continue
                        elif target_skill.GetAttackLevel() >= self.GetAttackLevel():
                            # 遇到高级攻击无效
                            continue

                else:  # 是群体攻击
                    if target_skill.GetAttackLevel() >= self.GetAttackLevel():
                        # 遇到高级攻击无效
                        continue

            elif isinstance(target_skill, DefenseSkill):
                # 针对防御等级
                if game.players[target_id].defense_level >= 1:  # "高防"
                    continue  # 无效化
            elif isinstance(target_skill, CommandSkill):
                pass

            game.players[caster_id].ChangeHealth(times * 1)
            game.players[target_id].ChangeHealth(-times * 1)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillXixue.GetSkillID().value] = SkillXixue
Skill_Name_To_ID[SkillXixue.GetName()] = SkillXixue.GetSkillID().value
