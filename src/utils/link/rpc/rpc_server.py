import src.utils.link.stub.gamelink_pb2 as plpb2
import src.utils.link.stub.gamelink_pb2_grpc as plpb2grpc

from src.models.battle.game import Game, Player
from src.models.battle.skill import Skill
from src.models.task_pool import TaskPool
from src.utils.link.rpc.rpc_linker import RpcLinker

from src.constant.config.conf import Cfg
import src.utils.logging.utils as Logging
from src.battle.choose_skill import ParserSkill
from src.utils.link.display import PrintMsgByID, PrintLobbyByPb2
import src.utils.link.display as Display
from src.utils.link.player_loop import SendThingsForever

import src.storage.battle as SBA
import src.storage.lobby as SLB
import src.storage.signal as Signal

import grpc
import pickle
import asyncio

from typing import Iterable


# Uid_Msg_dict: dict[int, asyncio.Queue] = {}
# MsgPool: TaskPool = TaskPool()


class Communicator(plpb2grpc.CommunicationServicer):

    def __init__(
        self,
        msg_sub_list: list[asyncio.Queue],
        sub_lock: asyncio.Lock,
        any_new: list[asyncio.Event],
        game_subs: list[asyncio.Queue],
    ) -> None:
        super().__init__()
        self.msg_subs = msg_sub_list
        self.lock = sub_lock
        self.any_news = any_new
        self.game_subs = game_subs

    async def Send_Action(
        self, request: plpb2.ActionSend, context: grpc.aio.ServicerContext
    ) -> plpb2.GeneralReply:
        ok, msg, sk = ParserSkill(request.uid, request.args, SBA.Current_Game)
        if ok is False or sk is None:
            return plpb2.GeneralReply(
                status=False, msg=f"Fail to summon skill to send: {msg}"
            )

        """加入游戏,之后还要触发一次判断是否所有人都做出了选择"""
        await GameUpdate(sk, self.game_subs, self.lock, self.any_news)
        return plpb2.GeneralReply(status=True, msg="success")

    async def Send_Message(
        self, request: plpb2.MsgSend, context: grpc.aio.ServicerContext
    ) -> plpb2.GeneralReply:
        # 显示给自己
        Display.PrintMsgByID(request.uid, request.content)
        # 广播
        async with self.lock:
            for sub in self.msg_subs:
                try:
                    sub.put_nowait((request.uid, request.content))
                except asyncio.QueueFull:
                    Logging.Warnln("Somebody's message queue is full")
                    continue
            for new_lock in self.any_news:
                new_lock.set()

        return plpb2.GeneralReply(status=True, msg="success")


class Linker(plpb2grpc.LinkerServicer):

    def __init__(
        self,
        msg_subs: list[asyncio.Queue],
        lob_subs: list[asyncio.Queue],
        game_subs: list[asyncio.Queue],
        sub_lock: asyncio.Lock,
        any_new: list[asyncio.Event],
    ) -> None:
        super().__init__()
        self.msg_subs = msg_subs
        self.lob_subs = lob_subs
        self.game_subs = game_subs
        self.sub_lock = sub_lock
        self.any_news = any_new

    async def Join_Game(
        self, request: plpb2.LobbyPlayerRequest, context: grpc.aio.ServicerContext
    ):
        # 先分配一个uid回去
        name = request.name
        this_player = SLB.Current_Lobby.AddPlayer(name)
        uid = this_player.GetId()

        yield plpb2.ServerReply(playerAssign=plpb2.LobbyPlayerAssign(uid=uid))

        msg_sub = asyncio.Queue()
        lob_sub = asyncio.Queue()
        game_sub = asyncio.Queue()
        New_Msg_Lock = asyncio.Event()

        async with self.sub_lock:
            self.msg_subs.append(msg_sub)
            self.lob_subs.append(lob_sub)
            self.game_subs.append(game_sub)
            self.any_news.append(New_Msg_Lock)

        Logging.Infoln(f"New Player {uid}/{name}")
        # 更新大厅
        SLB.DisplayLobby()
        new_lob = GetLobbyList()
        async with self.sub_lock:
            for sub in self.lob_subs:
                try:
                    sub.put_nowait(new_lob)
                except asyncio.QueueFull:
                    Logging.Warnln("Somebody's lobby queue is full")
                    continue
            for new_lock in self.any_news:
                new_lock.set()

        # [消费者Consumer]针对一名玩家的服务器返回
        try:
            while True:
                await New_Msg_Lock.wait()
                New_Msg_Lock.clear()

                if context.done():
                    # disconnect
                    Logging.Infoln(f"Client disconnected[{uid}/{name}]")
                    break

                # mass content here
                # 1. forward lobby
                while not lob_sub.empty():
                    try:
                        lob = lob_sub.get_nowait()
                    except asyncio.QueueEmpty:
                        break
                    yield plpb2.ServerReply(recvLobby=plpb2.LobbyStatus(players=lob))

                # 2. forward message
                while not msg_sub.empty():
                    try:
                        m_uid, m_msg = msg_sub.get_nowait()
                    except asyncio.QueueEmpty:
                        break
                    yield plpb2.ServerReply(
                        recvMsg=plpb2.MsgSend(uid=m_uid, content=m_msg)
                    )

                # 3. forward game
                while not game_sub.empty():
                    try:
                        game = game_sub.get_nowait()
                    except asyncio.QueueEmpty:
                        break
                    yield plpb2.ServerReply(recvGame=plpb2.GameStatus(game=game))

        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.CANCELLED:
                Logging.Infoln(f"Client cancelled strean [{uid}/{name}]")
            else:
                Logging.Errorln(f"RPC error: {e} [[{uid}/{name}]")


class RpcServer(RpcLinker):
    def __init__(self) -> None:
        super().__init__()
        self.Uid_Msg_dict = {}

        # 订阅者
        self.Sub_lock: asyncio.Lock = asyncio.Lock()
        self.Msg_Subs: list[asyncio.Queue] = []
        self.Lobby_Subs: list[asyncio.Queue] = []
        self.Game_Subs: list[asyncio.Queue] = []
        self.AnyMsgLock: list[asyncio.Event] = []

        self.linker = Linker(
            self.Msg_Subs,
            self.Lobby_Subs,
            self.Game_Subs,
            self.Sub_lock,
            self.AnyMsgLock,
        )
        self.Communicator = Communicator(
            self.Msg_Subs, self.Sub_lock, self.AnyMsgLock, self.Game_Subs
        )

        self.is_host = True

    async def serve(self, addr: str) -> None:
        server = grpc.aio.server()
        plpb2grpc.add_CommunicationServicer_to_server(self.Communicator, server)
        plpb2grpc.add_LinkerServicer_to_server(
            self.linker,
            server,
        )

        server.add_insecure_port(addr)
        Logging.Infoln(f"Starting server on {addr}")
        await server.start()
        await server.wait_for_termination()

    async def SendAction(self, skargs: str, sk: Skill):
        await GameUpdate(sk, self.Game_Subs, self.Sub_lock, self.AnyMsgLock)
        Display.PrintSentSkill(sk)

    async def SendMessage(self, msg: str):
        uid = SLB.My_Player_Info.GetId()
        # 显示给自己
        Display.PrintMsgByID(uid, msg)
        # 广播
        async with self.Sub_lock:
            for sub in self.Msg_Subs:
                try:
                    sub.put_nowait((uid, msg))
                except asyncio.QueueFull:
                    Logging.Warnln("Somebody's message queue is full")
                    continue
            for new_lock in self.AnyMsgLock:
                new_lock.set()

    async def JoinLobby(self):
        # Logging.Infoln("open")
        addr: str = str(Cfg["address"]["host_ip"]) + ":" + str(Cfg["address"]["port"])

        SLB.Current_Lobby = SLB.Lobby()
        SLB.My_Player_Info = SLB.Current_Lobby.AddPlayer(
            Cfg["player_info"]["player_name"]
        )
        asyncio.create_task(self.serve(addr))
        await SendThingsForever(self)

    async def StartGame(self):
        SBA.Current_Game = Game(Cfg["gamerule"])
        args = SLB.Current_Lobby.GetGameArgs()
        for uid, pname in args:
            SBA.Current_Game.AddPlayer(Player(pname, uid))

        SBA.Current_Game.OnRoundStart()

        game_bytes = pickle.dumps(SBA.Current_Game)

        async with self.Sub_lock:
            for sub in self.Game_Subs:
                await sub.put(game_bytes)
            for new_lock in self.AnyMsgLock:
                new_lock.set()

        Display.PrintNewRoundByGame()

        # 判断游戏结束/自己是否4了
        if SBA.Current_Game.is_game_end:
            Display.PrintGameEnd()
        else:
            is_dead = SBA.Current_Game.players[SLB.My_Player_Info.GetId()].Health < 0
            Display.PrintReadyTips(is_dead)
            if not is_dead:  # 没死
                Signal.could_send_action.set()


def GetLobbyList() -> Iterable[plpb2.LobbyPlayer]:
    ret: list[plpb2.LobbyPlayer] = []
    lack_set = set()
    for lac in SLB.Current_Lobby.lack:
        lack_set.add(lac)

    for pl in SLB.Current_Lobby.player_infos:
        uid = pl.GetId()
        name = pl.GetName()
        ret.append(plpb2.LobbyPlayer(uid=uid, name=name, is_leave=(uid in lack_set)))

    return ret


async def GameUpdate(
    sk: Skill,
    game_sub: list[asyncio.Queue],
    lock: asyncio.Lock,
    any_news: list[asyncio.Event],
):
    """判断所有玩家是否准备完毕,并触发一次更新"""
    SBA.Current_Game.AddSkill(sk)
    # if 人没齐
    is_all_ready = SBA.Current_Game.HasAllLivePlayerDone(SLB.Current_Lobby)
    if is_all_ready:
        SBA.Current_Game.OnRoundEnd()
        SBA.Current_Game.OnRoundStart()
        SBA.Current_Game.is_game_end = (
            len(SBA.Current_Game.GetALiveUIDs(SLB.Current_Lobby)) <= 1
        )

        game_bytes = pickle.dumps(SBA.Current_Game)

        async with lock:
            for sub in game_sub:
                await sub.put(game_bytes)
            for new_lock in any_news:
                new_lock.set()

        Display.PrintNewRoundByGame()

        # 判断游戏结束/自己是否4了
        if SBA.Current_Game.is_game_end:
            Display.PrintGameEnd()
        else:
            is_dead = SBA.Current_Game.players[SLB.My_Player_Info.GetId()].Health < 0
            Display.PrintReadyTips(is_dead)
            if not is_dead:  # 没死
                Signal.could_send_action.set()
