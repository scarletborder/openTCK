from src.models.battle.player import Player
from src.models.battle.skill import Skill, AttackSkill
from src.battle.skills import Skill_Table, ImportSkillTable
import src.utils.judge_skill_type as jst
from prettytable import PrettyTable
from src.constant.enum.skill import SkillID, int_to_enum


class Game:
    def __init__(self):
        self.players: dict[int, Player] = {}
        self.Skill_Stash = SkillStash()

    def AddPlayer(self, player: Player):
        self.players[player.id] = player

    def GetStatus(self) -> PrettyTable:
        """展示场上每个玩家的属性"""
        table = PrettyTable()
        table.field_names = ["id", "name", "Health", "Point"]
        for t_id, t_player in self.players.items():
            table.add_row(
                [
                    f"{t_id}",
                    f"{t_player.Name}",
                    f"{t_player.Health}",
                    f"{t_player.Point}",
                ]
            )

        return table

    def OnRoundStart(self):
        self.Skill_Stash.reset()
        for pl in self.players.values():
            pl.OnRoundStart()

    def AddSkill(self, sk: "Skill") -> tuple[bool, str]:
        # tlist = self.Skill_Stash.caster_skill.get(caster_id, [])
        # # 多次技能只允许全为单体攻击
        # if len(tlist) > 0 and (jst.IsSingleByInt(skill_id) is not True):
        #     return False, "多次技能只允许全为单体攻击"

        # 是否缺少点数
        if self.players[sk.caster_id].Point < sk.GetPoint():
            # + self.Skill_Stash.GetPointRecord(caster_id):
            return False, "no enough point"

        # 成功添加
        self.Skill_Stash.caster_skill[sk.caster_id] = sk
        # tlist.append((target_id, int_to_enum(skill_id, SkillID, SkillID.SLEEP), times))
        # self.Skill_Stash.caster_skill[caster_id] = tlist
        # self.Skill_Stash.UpdatePointRecord(
        #     caster_id,
        #     self.Skill_Stash.GetPointRecord(caster_id)
        #     + Skill_Table[skill_id].GetPoint() * times,
        # )
        return True, ""

    def OnRoundEnd(self):
        self.calculateRoundResult()
        for pl in self.players.values():
            pl.OnRoundEnd()

    def calculateRoundResult(self):
        # 1. 看指令技能，设置trigger
        for caster_id, sk_v in self.Skill_Stash.caster_skill.items():
            if jst.IsCommand(sk_v.GetSkillID()):
                sk_v.Cast(self)
            # for sk in sk_v:
            #     if jst.IsCommand(sk[1]):
            #         Skill_Table[sk[1].value].Cast(caster_id, sk[0], sk[2], self)

        # 2. 看防御技能
        for caster_id, sk_v in self.Skill_Stash.caster_skill.items():
            if jst.IsDefense(sk_v.GetSkillID()):
                sk_v.Cast(self)

        # 3. 看攻击技能
        for caster_id, sk_v in self.Skill_Stash.caster_skill.items():
            if jst.IsSingle(sk_v.GetSkillID()) or jst.IsMulti(sk_v.GetSkillID()):
                sk_v.Cast(self)

        # Final. 使用技能耗费点数
        for caster_id, sk_v in self.Skill_Stash.caster_skill.items():
            self.players[caster_id].ChangePoint(-sk_v.GetPoint())

        return


class SkillStash:
    def __init__(self) -> None:
        self.caster_skill: dict[int, Skill] = {}  # 施法者id - 技能实例

        # # 统计人物这一局用过的点数
        # # self.point_record_dirty: dict[int, bool] = {}  # 减少重复计算
        # self.point_record: dict[int, int] = {}

    def reset(self):
        self.caster_skill = {}
        # for caster_id in self.point_record.keys():
        #     self.point_record[caster_id] = 0

    def Process(self, game: Game): ...

    # def IsPlayerUseSpecifiedSkillToPlayer(
    #     self, caster_id: int, target_id: int, skill_id: SkillID
    # ) -> tuple[bool, int]:
    #     vec = self.caster_skill.get(caster_id, [])
    #     for sk in vec:
    #         if sk[0] == target_id:
    #             if sk[1] == skill_id:
    #                 return True, sk[2]

    #     return False, 0

    def IsPlayerUseSpecifiedSkill(
        self, uid: int, skill_id: SkillID
    ) -> tuple[bool, Skill | None]:
        """判断某一id用户释放释放过某个技能"""
        sk = self.caster_skill.get(uid, None)
        if sk is not None:
            if sk.GetSkillID() == skill_id:
                return True, sk
            return False, None
        return False, None

    def GetTargetAttackLevel(self, target_id: int) -> int:
        """判断某目标的攻击等级(如果不是攻击技能永远为0)"""
        if (
            isinstance(self.caster_skill[target_id], AttackSkill) is True
        ):  # 是否是攻击技能
            return self.caster_skill[target_id].GetAttackLevel()  # type: ignore
        return 0

    # def UpdatePointRecord(self, caster_id, new_value):
    #     self.point_record[caster_id] = new_value

    # def GetPointRecord(self, caster_id):
    #     return self.point_record.get(caster_id, 0)


ImportSkillTable()  # Loading process
