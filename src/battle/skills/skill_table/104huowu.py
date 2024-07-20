# from src.models.battle.game import Game
from src.models.battle.skill import *
from src.constant.enum.skill import SkillType, SkillID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


class SkillHuowu(MultiAttackSkill):

    def __init__(self, caster_id: int, args: list, game: "Game|None" = None) -> None:
        """args为空"""
        super().__init__(caster_id, args)
        self.targets = list(game.GetLiveUIDs())
        self.targets.remove(self.caster_id)
        self.times = [1 for _ in range(len(self.targets))]

    @staticmethod
    def NewSkill(
        caster, args: list[str], game: "Game|None" = None
    ) -> tuple[bool, Skill | None, str]:
        if len(args) > 0:
            return False, None, "MULTI不需要任何参数"
        else:
            return True, SkillHuowu(caster, [], game), ""

    @staticmethod
    def GetTitle() -> str:
        """获取技能名称"""
        return "火舞"

    @staticmethod
    def GetName() -> str:
        return "huowu"

    @staticmethod
    def GetDescription() -> str:
        """获取技能描述"""
        return """群体攻击，所有目标-5"""

    @staticmethod
    def GetBasicPoint() -> int:
        return 5

    def GetPoint(self) -> int:
        """获取技能释放需要的点数"""
        return self.GetBasicPoint()  # AOE只需要算一次释放点数

    @staticmethod
    def GetSkillType() -> SkillType:
        return SkillType.MULTI

    @staticmethod
    def GetSkillID() -> SkillID:
        return SkillID.HUOWU

    @staticmethod
    def GetAttackLevel() -> int:
        return 5

    # 使用类
    def SingleCast(self, game: "Game", caster_id: int, target_id: int, times: int):
        target_skill, target_targets = game.Skill_Stash.GetTargetSkillDetail(target_id)

        if not self.IsValidToTarget(target_id):
            return
        
        if target_id == caster_id:  # 针对反弹
            game.players[target_id].ChangeHealth(-times * 5, game)
            return

        elif isinstance(target_skill, AttackSkill):
            if caster_id in target_targets:
                if (
                    target_skill.GetAttackLevel() >= self.GetAttackLevel()
                ):  # 遇到高级攻击无效
                    return
        elif isinstance(target_skill, DefenseSkill):
            # 针对防御等级
            if game.players[target_id].defense_level >= 2:
                return  # 无效化
        elif isinstance(target_skill, CommandSkill):
            if target_skill.GetSkillID() == SkillID.XIADU:
                return
            else:
                pass
        game.players[target_id].ChangeHealth(-times * 5, game)

    def Cast(self, game: "Game"):
        """在结算时候的释放技能"""
        for idx in range(len(self.targets)):
            tid = self.targets[idx]
            times = self.times[idx]
            self.SingleCast(game, self.caster_id, tid, times)


from src.battle.skills import Skill_Table, Skill_Name_To_ID  # noqa: E402

Skill_Table[SkillHuowu.GetSkillID().value] = SkillHuowu
Skill_Name_To_ID[SkillHuowu.GetName()] = SkillHuowu.GetSkillID().value
