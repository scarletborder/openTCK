from src.models.battle.player import Player
from src.models.battle.skill import (
    Skill,
    AttackSkill,
    SingleAttackSkill,
    MultiAttackSkill,
    DefenseSkill,
    CommandSkill,
)
import src.battle.skills as _
import src.utils.judge_skill_type as jst
from src.utils.cmd_skill_queue import GetCMDQueue
from src.utils.lobby import Lobby
from prettytable import PrettyTable
from src.constant.enum.skill import SkillID, int_to_enum
from src.constant.enum.battle_trigger import TriggerType
from typing import TYPE_CHECKING
from src.models.battle.trigger import (
    BattleTrigger,
    SpecifiedSkillTrigger,
    SpecifiedPlayerTrigger,
    SpecifiedTargetTrigger,
)
from src.constant.config.conf import Cfg
from src.constant.enum.battle_tag import TagEvent


class Game:
    def __init__(self):
        self.players: dict[int, Player] = {}
        self.Skill_Stash = SkillStash()
        self.Trigger_Stash = TriggerStash()
        self.Player_Status = ""
        self.Skill_Used_Times = {}  # 用于每个Round中记录技能使用次数
        self.context = {}
        self.turns = 0

    def AddPlayer(self, player: Player):
        self.players[player.id] = player

    # def AddPlayerByID(self, uid:int):
    #     self.players[uid] = player

    def GetStatus(self):
        """展示场上每个玩家的属性"""
        return self.Player_Status

    def ResetAllAttr(self):
        """
        Resets all attributes related to skills and triggers in the game.
        """
        self.Skill_Used_Times = {}
        self.Skill_Stash.reset()
        self.Trigger_Stash.reset()

    def OnRoundStart(self):
        self.turns += 1
        # reset
        is_somebody_hurt = False
        for pl in self.players.values():
            if pl.is_health_change:
                is_somebody_hurt = True
            pl.OnRoundStart()

        if is_somebody_hurt and Cfg["gamerule"]["drain_when_hurt"]:
            self.TagEventChange()
            for pl in self.players.values():
                pl.Point = 0

        tmp_table = PrettyTable()
        tmp_table.field_names = ["id", "name", "Health", "Point"]
        for t_id, t_player in self.players.items():
            tmp_table.add_row(
                [
                    f"{t_id}",
                    f"{t_player.Name}",
                    f"{t_player.Health if t_player.Health >= 0 else 'dead'}",
                    f"{t_player.Point}",
                ]
            )

        self.Player_Status = tmp_table.get_formatted_string()
        self.ResetAllAttr()

    def GetLiveUIDs(self) -> list[int]:
        """获取所有活人的uid"""
        ret = []
        for uid, player_info in self.players.items():
            if player_info.Health >= 0:
                # 血大于0
                ret.append(uid)

        return ret

    def GetALiveUIDs(self, lobby: "Lobby") -> list[int]:
        """获取所有在线活人的uid"""
        ret = []
        for uid, player_info in self.players.items():
            if player_info.Health >= 0 and lobby.IsUidLeave(uid) is False:
                # 血大于等于0并且没有离开
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
        self.Skill_Stash.caster_skill[sk.caster_id] = sk

    def AddTrigger(self, tri: "BattleTrigger"):
        # 判断是否是针对独特技能
        if isinstance(tri, SpecifiedSkillTrigger):
            if tri.Type == TriggerType.B_SPECIFIEDSKILL:
                tril = self.Trigger_Stash.b_skill_triggers.get(tri.sp_skid, [])
                tril.append(tri)
                self.Trigger_Stash.b_skill_triggers[tri.sp_skid] = tril
            else:
                tril = self.Trigger_Stash.p_skill_triggers.get(tri.sp_skid, [])
                tril.append(tri)
                self.Trigger_Stash.p_skill_triggers[tri.sp_skid] = tril
        elif isinstance(tri, SpecifiedPlayerTrigger):
            if tri.Type == TriggerType.B_SPECIFIEDPLAYER:
                tril = self.Trigger_Stash.b_player_triggers.get(tri.sp_plid, [])
                tril.append(tri)
                self.Trigger_Stash.b_player_triggers[tri.sp_plid] = tril
            else:
                tril = self.Trigger_Stash.p_player_triggers.get(tri.sp_plid, [])
                tril.append(tri)
                self.Trigger_Stash.p_player_triggers[tri.sp_plid] = tril
        elif isinstance(tri, SpecifiedTargetTrigger):
            if tri.Type == TriggerType.B_SPECIFIEDTARGET:
                tril = self.Trigger_Stash.b_target_triggers.get(tri.sp_tid, [])
                tril.append(tri)
                self.Trigger_Stash.b_target_triggers[tri.sp_tid] = tril
            else:
                tril = self.Trigger_Stash.p_target_triggers.get(tri.sp_tid, [])
                tril.append(tri)
                self.Trigger_Stash.p_target_triggers[tri.sp_tid] = tril
        else:
            tril = self.Trigger_Stash.misc_triggers.get(tri.Type, [])
            tril.append(tri)
            self.Trigger_Stash.misc_triggers[tri.Type] = tril

    def AddNextTrigger(self, tri: "BattleTrigger"):
        """向下一回合加入触发器"""
        # 判断是否是针对独特技能
        if isinstance(tri, SpecifiedSkillTrigger):
            if tri.Type == TriggerType.B_SPECIFIEDSKILL:
                tril = self.Trigger_Stash.Nb_skill_triggers.get(tri.sp_skid, [])
                tril.append(tri)
                self.Trigger_Stash.Nb_skill_triggers[tri.sp_skid] = tril
            else:
                tril = self.Trigger_Stash.Np_skill_triggers.get(tri.sp_skid, [])
                tril.append(tri)
                self.Trigger_Stash.Np_skill_triggers[tri.sp_skid] = tril
        elif isinstance(tri, SpecifiedPlayerTrigger):
            if tri.Type == TriggerType.B_SPECIFIEDPLAYER:
                tril = self.Trigger_Stash.Nb_player_triggers.get(tri.sp_plid, [])
                tril.append(tri)
                self.Trigger_Stash.Nb_player_triggers[tri.sp_plid] = tril
            else:
                tril = self.Trigger_Stash.Np_player_triggers.get(tri.sp_plid, [])
                tril.append(tri)
                self.Trigger_Stash.Np_player_triggers[tri.sp_plid] = tril
        elif isinstance(tri, SpecifiedTargetTrigger):
            if tri.Type == TriggerType.B_SPECIFIEDTARGET:
                tril = self.Trigger_Stash.Nb_target_triggers.get(tri.sp_tid, [])
                tril.append(tri)
                self.Trigger_Stash.Nb_target_triggers[tri.sp_tid] = tril
            else:
                tril = self.Trigger_Stash.Np_target_triggers.get(tri.sp_tid, [])
                tril.append(tri)
                self.Trigger_Stash.Np_target_triggers[tri.sp_tid] = tril
        else:
            tril = self.Trigger_Stash.Nmisc_triggers.get(tri.Type, [])
            tril.append(tri)
            self.Trigger_Stash.Nmisc_triggers[tri.Type] = tril

    def OnRoundEnd(self):
        self.Skill_Stash.MakeSkillLog()
        self.calculateRoundResult()
        for pl in self.players.values():
            pl.OnRoundEnd()

    def CheckTagEvent(self):
        for player_id in self.GetLiveUIDs():
            if self.players[player_id].tag.get(TagEvent.SHANDIAN, 0):
                if self.Skill_Used_Times.get(SkillID.XIADU, 0) >= 3:
                    self.players[player_id].InstantKill()
                    self.players[player_id].tag[TagEvent.SHANDIAN] = 0
    
    def TagEventChange(self):
        live_uids = self.GetLiveUIDs()
        num_players = len(live_uids)
        
        if num_players == 0:
            return

        # 创建一个列表来记录拥有 SHANDIAN 标签的玩家索引
        shandian_indices = []
        
        for i in range(num_players):
            if self.players[live_uids[i]].tag.get(TagEvent.SHANDIAN):
                shandian_indices.append(i)
        
        # 遍历所有拥有 SHANDIAN 标签的玩家并将其传递给下一个玩家
        for i in shandian_indices:
            current_player = self.players[live_uids[i]]
            current_player.tag[TagEvent.SHANDIAN] = 0
            next_player = self.players[live_uids[(i + 1) % num_players]]
            next_player.tag[TagEvent.SHANDIAN] = 1

            


    def calculateRoundResult(self):
        # 排序指令性技能
        cmd_skills: list[CommandSkill] = []
        for sk_v in self.Skill_Stash.caster_skill.values():
            if isinstance(sk_v, CommandSkill):
                cmd_skills.append(sk_v)
        cmd_skills = GetCMDQueue(cmd_skills)

        # 1. 看指令技能
        for sk_v in cmd_skills:
            if sk_v.CouldCmdCast(1):
                caster_id = sk_v.caster_id
                try:
                    CastSkill(self, sk_v)
                except BaseException as e:
                    # 执行技能出错
                    self.Skill_Stash.sk_error += f"\nerror in {caster_id}/{self.players[caster_id].Name} use {sk_v.GetName()}: {e}"

        # TagEvent
        self.CheckTagEvent()

        # 2. 看防御技能
        for caster_id, sk_v in self.Skill_Stash.caster_skill.items():
            if isinstance(sk_v, DefenseSkill):
                try:
                    CastSkill(self, sk_v)
                except BaseException as e:
                    self.Skill_Stash.sk_error += f"\nerror in {caster_id}/{self.players[caster_id].Name} use {sk_v.GetName()}: {e}"

        # 3. 看攻击技能
        for caster_id, sk_v in self.Skill_Stash.caster_skill.items():
            if isinstance(sk_v, AttackSkill):
                try:
                    CastSkill(self, sk_v)
                except BaseException as e:
                    self.Skill_Stash.sk_error += f"\nerror in {caster_id}/{self.players[caster_id].Name} use {sk_v.GetName()}: {e}"

        # 4. 看指令技能
        for sk_v in cmd_skills:
            if sk_v.CouldCmdCast(4):
                caster_id = sk_v.caster_id
                try:
                    CastSkill(self, sk_v)
                except BaseException as e:
                    # 执行技能出错
                    self.Skill_Stash.sk_error += f"\nerror in {caster_id}/{self.players[caster_id].Name} use {sk_v.GetName()}: {e}"

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

    def GetHurtPlayers(self) -> list[int]:
        return [k for k, v in self.players.items() if v.is_hurt]
    
    def GetPlayerTag(self, player_id):
        return self.players[player_id].tag.keys(), self.players[player_id].tag.values()


class SkillStash:
    def __init__(self) -> None:
        self.caster_skill: dict[int, Skill] = {}  # 施法者id - 技能实例
        self.sk_log = ""
        self.sk_error = ""

        # # 统计人物这一局用过的点数
        # # self.point_record_dirty: dict[int, bool] = {}  # 减少重复计算
        # self.point_record: dict[int, int] = {}

    def reset(self):
        self.caster_skill.clear()

        # for caster_id in self.point_record.keys():
        #     self.point_record[caster_id] = 0

    def ResetLog(self):
        self.sk_log = ""
        self.sk_error = ""

    def Process(self, game: Game): ...

    def MakeSkillLog(self):
        self.ResetLog()
        self.sk_log = "\n".join([str(_) for _ in self.caster_skill.values()])

    def GetSkillStatus(self) -> str:
        """查看回合内技能的使用情况和错误日志"""
        return self.sk_log + self.sk_error

    # def IsPlayerUseSpecifiedSkillToPlayer(
    #     self, caster_id: int, target_id: int, skill_id: SkillID
    # ) -> tuple[bool, int]:
    #     vec = self.caster_skill.get(caster_id, [])
    #     for sk in vec:
    #         if sk[0] == target_id:
    #             if sk[1] == skill_id:
    #                 return True, sk[2]

    #     return False, 0

    def GetTargetSkillDetail(self, target: int) -> tuple[Skill | None, list[int]]:
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


class TriggerStash:
    def __init__(self) -> None:
        self.misc_triggers: dict["TriggerType", list["BattleTrigger"]] = {}
        self.b_skill_triggers: dict[SkillID, list["BattleTrigger"]] = {}
        self.p_skill_triggers: dict[SkillID, list["BattleTrigger"]] = {}
        self.b_player_triggers: dict[int, list["BattleTrigger"]] = {}
        self.p_player_triggers: dict[int, list["BattleTrigger"]] = {}
        self.b_target_triggers: dict[int, list["BattleTrigger"]] = {}
        self.p_target_triggers: dict[int, list["BattleTrigger"]] = {}

        self.Nmisc_triggers: dict["TriggerType", list["BattleTrigger"]] = {}
        self.Nb_skill_triggers: dict[SkillID, list["BattleTrigger"]] = {}
        self.Np_skill_triggers: dict[SkillID, list["BattleTrigger"]] = {}
        self.Nb_player_triggers: dict[int, list["BattleTrigger"]] = {}
        self.Np_player_triggers: dict[int, list["BattleTrigger"]] = {}
        self.Nb_target_triggers: dict[int, list["BattleTrigger"]] = {}
        self.Np_target_triggers: dict[int, list["BattleTrigger"]] = {}

    def reset(self):
        self.misc_triggers = self.Nmisc_triggers.copy()
        self.b_skill_triggers = self.Nb_skill_triggers.copy()
        self.p_skill_triggers = self.Np_skill_triggers.copy()
        self.b_player_triggers = self.Nb_player_triggers.copy()
        self.p_player_triggers = self.Np_player_triggers.copy()
        self.b_target_triggers = self.Nb_target_triggers.copy()
        self.p_target_triggers = self.Np_target_triggers.copy()

        self.Nmisc_triggers.clear()
        self.Nb_skill_triggers.clear()
        self.Np_skill_triggers.clear()
        self.Nb_player_triggers.clear()
        self.Np_player_triggers.clear()
        self.Nb_target_triggers.clear()
        self.Np_target_triggers.clear()


def CastSkill(game: Game, sk_v: "Skill"):
    """触发技能，考虑到了触发可能的触发器"""
    att_flag: bool = False
    if isinstance(sk_v, AttackSkill):
        # 如果是攻击技能
        att_flag = True

    # 特定用户
    tril = game.Trigger_Stash.b_player_triggers.get(sk_v.caster_id, [])
    for tri in tril:
        tri.Cast(game, sk_v)

    # 特定目标
    if hasattr(sk_v, "targets"):
        # print(sk_v.GetTitle(), sk_v.targets)
        for target in sk_v.targets:
            tril = game.Trigger_Stash.b_target_triggers.get(target, [])
            for tri in tril:
                tri.Cast(game, sk_v)

    # 攻击技能
    if att_flag:
        tril = game.Trigger_Stash.misc_triggers.get(TriggerType.B_ATTACKSKILL, [])
        for tri in tril:
            tri.Cast(game, sk_v)

    # 特定技能
    tril = game.Trigger_Stash.b_skill_triggers.get(sk_v.GetSkillID(), [])
    for tri in tril:
        tri.Cast(game, sk_v)

    sk_v.Cast(game)

    # 特定技能
    tril = game.Trigger_Stash.p_skill_triggers.get(sk_v.GetSkillID(), [])
    for tri in tril:
        tri.Cast(game, sk_v)

    # 攻击技能
    if att_flag:
        tril = game.Trigger_Stash.misc_triggers.get(TriggerType.P_ATTACKSKILL, [])
        for tri in tril:
            tri.Cast(game, sk_v)

    # 特定目标
    tril = game.Trigger_Stash.p_target_triggers.get(sk_v.caster_id, [])
    for tri in tril:
        tri.Cast(game, sk_v)

    # 特定用户
    tril = game.Trigger_Stash.p_player_triggers.get(sk_v.caster_id, [])
    for tri in tril:
        tri.Cast(game, sk_v)
