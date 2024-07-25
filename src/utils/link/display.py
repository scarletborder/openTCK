# from src.models.link.link_data import MessageData

# def DataToMessage(data: MessageData)->str:
#     # 需要从Lobby中读取用户Uid对应的名字
#     data.

import src.utils.link.stub.gamelink_pb2 as plpb2
import src.storage.lobby as SLB
import src.storage.battle as SBA
from src.models.battle.skill import Skill
from src.utils.pkui.utils import NewUI
from src.utils.lobby import Lobby
import src.utils.logging.utils as Logging


def PrintMsgByID(uid: int, msg: str) -> None:
    PrintMsgByname(SLB.Current_Lobby.player_infos[uid].name, msg)


def PrintMsgByname(name: str, msg: str) -> None:
    NewUI.PrintChatArea(f"{name}:{msg}")


def PrintLobbyByPb2(lobby_pb2: plpb2.LobbyStatus):
    """更新并打印新的大厅"""
    new_lobby = Lobby.NewFromPb2(lobby_pb2)
    SLB.Current_Lobby = new_lobby  # 更新大厅
    SLB.DisplayLobby()


def PrintNewRoundByGame():
    if SBA.Current_Game.turns == 1:
        # new game
        Logging.Infoln("#" * 5 + "New game begins" + "#" * 5)
    NewUI.PrintChatArea("=" * 5 + f"Round {SBA.Current_Game.turns}" + "=" * 5)
    NewUI.PrintChatArea(SBA.Current_Game.Skill_Stash.GetSkillStatus())
    NewUI.PrintStatusArea(SBA.Current_Game.GetStatus())


def PrintReadyTips(is_dead: bool):
    if is_dead:
        NewUI.PrintTipArea("你的角色已经阵亡")
    else:
        NewUI.PrintTipArea("请输出技能")


def PrintSentSkill(sk: Skill):
    NewUI.PrintTipArea(str(sk))


def PrintGameEnd():
    lids = SBA.Current_Game.GetALiveUIDs(SLB.Current_Lobby)
    if len(lids) <= 1:
        if len(lids) == 1:
            NewUI.PrintChatArea(
                f"游戏结束了,{SBA.Current_Game.players[lids[0]].Name}是Winner\nhost输入start再开一把"
            )
        else:
            NewUI.PrintChatArea("人员全部离线，游戏结束")
