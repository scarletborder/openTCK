from src.models.battle.player import Player
from src.models.battle.skill import Skill, AttackSkill, SingleAttackSkill
from src.battle.skills import Skill_Table, ImportSkillTable
import src.utils.judge_skill_type as jst
from src.utils.lobby import Lobby
from prettytable import PrettyTable
from src.constant.enum.skill import SkillID, int_to_enum


class Game:
    def __init__(self):
        self.players: dict[int, Player] = {}
        self.Skill_Stash = SkillStash()

    def AddPlayer(self, player: Player):
        self.players[player.id] = player

    # def AddPlayerByID(self, uid:int):
    #     self.players[uid] = player

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
        # reset
        self.Skill_Stash.reset()
        for pl in self.players.values():
            pl.OnRoundStart()

    def GetLiveUIDs(self) -> list[int]:
        """获取所有活人的uid"""
        ret = []
        for uid, player_info in self.players.items():
            if player_info.Health > 0:
                # 血大于0
                ret.append(uid)

        return ret

    def GetALiveUIDs(self, lobby: "Lobby") -> list[int]:
        """获取所有在线活人的uid"""
        ret = []
        for uid, player_info in self.players.items():
            if player_info.Health > 0 and lobby.IsUidLeave(uid) is False:
                # 血大于0并且没有离开
                ret.append(uid)

        return ret

    def JudgeAddSkill(self, sk: "Skill") -> tuple[bool, str]:
        """判断当前状态下是否能加入技能"""
        # 是否缺少点数
        if self.players[sk.caster_id].Point < sk.GetPoint():
            # + self.Skill_Stash.GetPointRecord(caster_id):
            return False, "no enough point"
        else:
            return True, ""

        # 冰冻效果只能sleep

    def AddSkill(self, sk: "Skill"):
        # tlist = self.Skill_Stash.caster_skill.get(caster_id, [])
        # # 多次技能只允许全为单体攻击
        # if len(tlist) > 0 and (jst.IsSingleByInt(skill_id) is not True):
        #     return False, "多次技能只允许全为单体攻击"

        # 成功添加
        self.Skill_Stash.caster_skill[sk.caster_id] = sk
        # tlist.append((target_id, int_to_enum(skill_id, SkillID, SkillID.SLEEP), times))
        # self.Skill_Stash.caster_skill[caster_id] = tlist
        # self.Skill_Stash.UpdatePointRecord(
        #     caster_id,
        #     self.Skill_Stash.GetPointRecord(caster_id)
        #     + Skill_Table[skill_id].GetPoint() * times,
        # )
        # return True, ""

    def OnRoundEnd(self):
        self.calculateRoundResult()
        for pl in self.players.values():
            pl.OnRoundEnd()

    def calculateRoundResult(self):
        # 1. 看指令技能，设置trigger
        for caster_id, sk_v in self.Skill_Stash.caster_skill.items():
            if jst.IsCommand(sk_v.GetSkillID()):
                try:
                    sk_v.Cast(self)
                except BaseException as e:
                    # 执行技能出错
                    self.Skill_Stash.sk_error += f"error in {caster_id}/{self.players[caster_id].Name} use {sk_v.GetName()}: {e}\n"
                    ...
            # for sk in sk_v:
            #     if jst.IsCommand(sk[1]):
            #         Skill_Table[sk[1].value].Cast(caster_id, sk[0], sk[2], self)

        # 2. 看防御技能
        for caster_id, sk_v in self.Skill_Stash.caster_skill.items():
            if jst.IsDefense(sk_v.GetSkillID()):
                try:
                    sk_v.Cast(self)
                except BaseException as e:
                    self.Skill_Stash.sk_error += f"error in {caster_id}/{self.players[caster_id].Name} use {sk_v.GetName()}: {e}\n"

        # 3. 看攻击技能
        for caster_id, sk_v in self.Skill_Stash.caster_skill.items():
            if jst.IsSingle(sk_v.GetSkillID()) or jst.IsMulti(sk_v.GetSkillID()):
                try:
                    sk_v.Cast(self)
                except BaseException as e:
                    self.Skill_Stash.sk_error += f"error in {caster_id}/{self.players[caster_id].Name} use {sk_v.GetName()}: {e}\n"

        # Final. 使用技能耗费点数
        for caster_id, sk_v in self.Skill_Stash.caster_skill.items():
            self.players[caster_id].ChangePoint(-sk_v.GetPoint())

        return

    def HasAllLivePlayerDone(self, lobby: "Lobby") -> bool:
        """所有在线的存活玩家是否完成了释放技能"""
        for uid, player_info in self.players.items():
            if player_info.Health > 0:
                if (
                    uid not in self.Skill_Stash.caster_skill.keys()  # 没有释放技能
                ) and lobby.IsUidLeave(uid) is False:
                    # 并且没有离开
                    return False

        return True


class SkillStash:
    def __init__(self) -> None:
        self.caster_skill: dict[int, Skill] = {}  # 施法者id - 技能实例
        self.sk_error = ""

        # # 统计人物这一局用过的点数
        # # self.point_record_dirty: dict[int, bool] = {}  # 减少重复计算
        # self.point_record: dict[int, int] = {}

    def reset(self):
        self.caster_skill = {}
        self.sk_error = ""
        # for caster_id in self.point_record.keys():
        #     self.point_record[caster_id] = 0

    def Process(self, game: Game): ...

    def GetSkillStatus(self) -> str:
        """查看回合内技能的使用情况和错误日志"""
        return "\n".join([str(_) for _ in self.caster_skill.values()]) + self.sk_error

    # def IsPlayerUseSpecifiedSkillToPlayer(
    #     self, caster_id: int, target_id: int, skill_id: SkillID
    # ) -> tuple[bool, int]:
    #     vec = self.caster_skill.get(caster_id, [])
    #     for sk in vec:
    #         if sk[0] == target_id:
    #             if sk[1] == skill_id:
    #                 return True, sk[2]

    #     return False, 0

    def getTargetSkillDetail(self, target: int) -> tuple[Skill | None, list[int]]:
        """获取某个目标的单体技能实例和其选定的目标们"""
        sk = self.caster_skill[target]
        if isinstance(sk, AttackSkill):
            return sk, sk.targets
        return sk, []

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

    def GetTargetAttackLevel(self, uid: int, target: int) -> int:
        """判断某人向某个目标的攻击等级(如果不是攻击技能永远为0)"""
        sk = self.caster_skill[uid]
        if isinstance(sk, AttackSkill) is True:  # 是否是攻击技能
            if isinstance(sk, SingleAttackSkill) is True:  # 是单体
                if target in sk.targets:  # type: ignore
                    return sk.GetAttackLevel()
                else:
                    return 0
            else:  # 是群体
                return sk.GetAttackLevel()  # type: ignore
        return 0

    # def UpdatePointRecord(self, caster_id, new_value):
    #     self.point_record[caster_id] = new_value

    # def GetPointRecord(self, caster_id):
    #     return self.point_record.get(caster_id, 0)


ImportSkillTable()  # Loading process
