import src.utils.link.stub.gamelink_pb2 as plpb2
import src.utils.link.stub.gamelink_pb2_grpc as plpb2grpc

from src.models.battle.game import Game
from src.models.battle.skill import Skill
from src.models.task_pool import TaskPool
from src.utils.link.rpc.rpc_linker import RpcLinker

from src.constant.config.conf import Cfg
import src.utils.logging.utils as Logging
from src.utils.link.display import PrintMsgByID, PrintLobbyByPb2
import src.utils.link.display as Display

import src.storage.battle as SBA
import src.storage.lobby as SLB
import src.storage.signal as Signal

import grpc
import pickle
import asyncio

# GTask_Pool = TaskPool()
addr = ""


async def run() -> None:
    """JoinLobby的gRPC版本

    包含向服务端发送一个登录的请求,并获得一个可以返回很多信息的流

    这个流式返回参数将被解析为不同的类型
    """
    global addr
    host_ip = Cfg["address"]["host_ip"]
    port = Cfg["address"]["port"]
    my_name = Cfg["player_info"]["player_name"]
    SLB.My_Player_Info.name = my_name
    addr = f"{host_ip}:{port}"
    SLB.Is_Host = False

    async with grpc.aio.insecure_channel(addr) as channel:
        stub = plpb2grpc.LinkerStub(channel)
        # asyncio.create_task(send_loop(stub))

        # Read from an async generator
        async for response in stub.Join_Game(plpb2.LobbyPlayerRequest(my_name)):
            ProcessResponse(response)


async def ProcessResponse(resp: plpb2.ServerReply) -> None:
    if resp.HasField("linkStatus"):
        # 连接状态
        if not resp.linkStatus.status:
            Logging.Errorln("Link failed: " + resp.linkStatus.msg)

    elif resp.HasField("playerAssign"):
        SLB.My_Player_Info.id = resp.playerAssign.uid
        Logging.Infoln("You have succeed joining the game")

    elif resp.HasField("recvMsg"):
        PrintMsgByID(resp.recvMsg.uid, resp.recvMsg.content)

    elif resp.HasField("recvLobby"):
        # LinkEvent.LOBBYUPDATE
        PrintLobbyByPb2(resp.recvLobby)

    elif resp.HasField("recvGame"):
        game: Game = pickle.loads(resp.recvGame.game)
        SBA.Current_Game = game
        # 接受到游戏信息,表示游戏开始或者是新回合开始
        Display.PrintNewRoundByGame()

        # 判断游戏结束/自己是否4了
        if SBA.Current_Game.is_game_end:
            Display.PrintGameEnd()
        else:
            is_dead = SBA.Current_Game.players[SLB.My_Player_Info.GetId()].Health < 0
            Display.PrintReadyTips(is_dead)
            if not is_dead:  # 没死
                Signal.could_send_action.set()

    else:
        Logging.Errorln(f"Unexpected response {resp}")  # error


class RpcClient(RpcLinker):
    async def SendAction(self, skargs: str, sk: Skill):
        # 先发
        async with grpc.aio.insecure_channel(addr) as channel:
            stub = plpb2grpc.CommunicationStub(channel)
            resp: "plpb2.GeneralReply" = await stub.Send_Action(
                plpb2.ActionSend(uid=SLB.My_Player_Info.id, args=skargs)
            )
            if resp.status:
                Display.PrintSentSkill(sk)
            else:
                Logging.Errorln(f"Fail in send skill: {resp.msg}")
            Signal.could_send_action.set()  # 重新允许输入技能

    async def SendMessage(self, msg: str):
        async with grpc.aio.insecure_channel(addr) as channel:
            stub = plpb2grpc.CommunicationStub(channel)
            resp: "plpb2.GeneralReply" = await stub.Send_Message(
                plpb2.MsgSend(uid=SLB.My_Player_Info.id, content=msg)
            )
            if not resp.status:
                Logging.Errorln(f"Fail in send message: {resp.msg}")
