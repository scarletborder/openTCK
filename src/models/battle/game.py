from src.models.battle.player import Player
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

    def AddSkill(
        self, caster_id: int, target_id: int, times: int, skill_id: int
    ) -> tuple[bool, str]:
        tlist = self.Skill_Stash.caster_skill.get(caster_id, [])
        # 多次技能只允许全为单体攻击
        if len(tlist) > 0 and (jst.IsSingleByInt(skill_id) is not True):
            return False, "多次技能只允许全为单体攻击"

        # 是否缺少点数
        if (
            self.players[caster_id].Point
            < self.Skill_Stash.GetPointRecord(caster_id)
            + Skill_Table[skill_id].GetPoint() * times
        ):
            return False, "no enough point"

        # 成功添加
        tlist.append((target_id, int_to_enum(skill_id, SkillID, SkillID.SLEEP), times))
        self.Skill_Stash.caster_skill[caster_id] = tlist
        self.Skill_Stash.UpdatePointRecord(
            caster_id,
            self.Skill_Stash.GetPointRecord(caster_id)
            + Skill_Table[skill_id].GetPoint() * times,
        )
        return True, ""

    def OnRoundEnd(self):
        self.calculateRoundResult()
        for pl in self.players.values():
            pl.OnRoundEnd()

    def calculateRoundResult(self):
        # 1. 看指令技能，设置trigger
        for caster_id, sk_v in self.Skill_Stash.caster_skill.items():
            for sk in sk_v:
                if jst.IsCommand(sk[1]):
                    Skill_Table[sk[1].value].Cast(caster_id, sk[0], sk[2], self)

        # 2. 看防御技能
        for caster_id, sk_v in self.Skill_Stash.caster_skill.items():
            for sk in sk_v:
                if jst.IsDefense(sk[1]):
                    Skill_Table[sk[1].value].Cast(caster_id, sk[0], sk[2], self)

        # 3. 看攻击技能
        for caster_id, sk_v in self.Skill_Stash.caster_skill.items():
            for sk in sk_v:
                if jst.IsSingle(sk[1]) or jst.IsMulti(sk[1]):
                    Skill_Table[sk[1].value].Cast(caster_id, sk[0], sk[2], self)

        # Final. 使用技能耗费点数
        for caster_id, used_point in self.Skill_Stash.point_record.items():
            self.players[caster_id].ChangePoint(-used_point)

        return


class SkillStash:
    def __init__(self) -> None:
        self.caster_skill: dict[int, list[tuple[int, SkillID, int]]] = (
            {}
        )  # 施法者id - [(目标id,技能id,使用次数)]

        # 统计人物这一局用过的点数
        # self.point_record_dirty: dict[int, bool] = {}  # 减少重复计算
        self.point_record: dict[int, int] = {}

    def reset(self):
        self.caster_skill = {}
        for caster_id in self.point_record.keys():
            self.point_record[caster_id] = 0

    def Process(self, game: Game): ...

    def IsPlayerUseSpecifiedSkillToPlayer(
        self, caster_id: int, target_id: int, skill_id: SkillID
    ) -> tuple[bool, int]:
        vec = self.caster_skill.get(caster_id, [])
        for sk in vec:
            if sk[0] == target_id:
                if sk[1] == skill_id:
                    return True, sk[2]

        return False, 0

    def UpdatePointRecord(self, caster_id, new_value):
        self.point_record[caster_id] = new_value

    def GetPointRecord(self, caster_id):
        return self.point_record.get(caster_id, 0)


ImportSkillTable()
