from abc import ABC, abstractmethod
from src.battle.choose_skill import ParserSkill
from src.models.battle.player import Player
from src.models.battle.game import Game
from src.models.link.link_data import (
    LinkData,
    MessageData,
    BattleActionData,
    BattleResultData,
    BattleStartData,
    LobbyUpdateData,
    LobbyAssignData,
    LinkEvent,
)
from src.models.battle.skill import Skill

from src.constant.config.conf import Cfg
import src.utils.link.link_menu as LM
from src.utils.lobby import Lobby
import src.storage.battle as SBA
import src.storage.lobby as SLB
import asyncio
import pickle
from src.storage.buffer import SetInput, ReadInput, TimesToReconnect

from src.utils.pkui.utils import NewUI


class PlayerLink(ABC):
    @abstractmethod
    def __init__(self):
        self.could_type = asyncio.Event()  # 是否可以输入字符
        self.could_send_action = asyncio.Event()  # 是否可以出招
        self.could_type.set()
        self.could_send_action.clear()
        self.is_host = False

    @abstractmethod
    async def JoinLobby(self): ...

    @abstractmethod
    async def Send(self, data): ...

    @abstractmethod
    async def SendAction(self, skill: Skill): ...

    @abstractmethod
    async def SendMessage(self, msg: str): ...


class HostPlayerLink(PlayerLink):
    def __init__(self):
        super().__init__()
        self.clients = []

    async def Send(self, data):
        await self.broadCast(data)

    async def broadCast(self, data, writer=None):
        for client in self.clients:
            if client != writer:
                client.write(pickle.dumps(data))
                await client.drain()

    async def JoinLobby(self):
        """作为host创建lobby

        1. 读取配置文件中的开放ip和port

        2. 尝试开放
        """
        self.host_ip = Cfg["address"]["host_ip"]
        self.port = Cfg["address"]["port"]
        self.is_host = True
        SLB.Current_Lobby = Lobby()
        SLB.My_Player_Info = SLB.Current_Lobby.AddPlayer(
            Cfg["player_info"]["player_name"]
        )
        self.clients = []

        self.Server = await asyncio.start_server(
            self.handle_client, self.host_ip, self.port
        )
        addr = self.Server.sockets[0].getsockname()
        NewUI.PrintChatArea(f"Serving on {addr}")

        self.could_type.set()
        self.could_send_action.clear()

        # gather forever
        async with self.Server:
            await asyncio.gather(self.Server.serve_forever(), SendThingsForever(self))

        NewUI.PrintChatArea("大厅已经关闭")

    async def StartGame(self):
        SBA.Current_Game = Game()
        args = SLB.Current_Lobby.GetGameArgs()
        for uid, pname in args:
            SBA.Current_Game.AddPlayer(Player(pname, uid))

        SBA.Current_Game.OnRoundStart()
        await self.broadCast(
            BattleStartData(SLB.My_Player_Info.GetId(), SBA.Current_Game)
        )
        NewUI.PrintStatusArea(SBA.Current_Game.GetStatus())
        self.could_send_action.set()
        NewUI.PrintChatArea("你可以发送技能了")
        NewUI.PrintTipArea("请输出技能")

    async def handle_client(self, reader, writer):
        self.clients.append(writer)
        addr = writer.get_extra_info("peername")
        NewUI.PrintChatArea(f"New client: {addr}")
        # 分配一个player_info
        new_player_info = SLB.Current_Lobby.AddPlayer()
        writer.write(
            pickle.dumps(
                LobbyAssignData(SLB.My_Player_Info.GetId(), new_player_info.GetId())
            )
        )
        await writer.drain()

        while True:
            data = []
            try:
                while not reader.at_eof():
                    try:
                        packet = await asyncio.wait_for(reader.read(4096), timeout=0.5)
                        if not packet:
                            NewUI.PrintChatArea("client disconnected")
                            break
                        data.append(packet)
                    except asyncio.CancelledError:
                        NewUI.PrintChatArea(f"Connection with {addr} was cancelled")
                        break
                    except ConnectionResetError:
                        NewUI.PrintChatArea(f"Connection with {addr} was reset by peer")
                        break
                    except asyncio.IncompleteReadError:
                        NewUI.PrintChatArea(f"Incomplete read error from {addr}")
                        break
                    except asyncio.TimeoutError:
                        break

                if reader.at_eof():
                    NewUI.PrintChatArea("client disconnected")
                    break

                if len(data) == 0:
                    continue

                recv_data: LinkData = pickle.loads(b"".join(data))

                parserd_data = recv_data.Parser()
                # 根据messageEvent来分支
                if recv_data.data_type == LinkEvent.CHATMESSAGE:
                    NewUI.PrintChatArea(
                        f"{recv_data.uid}/{SLB.Current_Lobby.player_infos[recv_data.uid].GetName()}:"
                        + parserd_data["msg"]
                    )

                    await self.broadCast(recv_data, writer)

                elif recv_data.data_type == LinkEvent.BATTLEACTION:
                    # 加入技能
                    SBA.Current_Game.AddSkill(parserd_data["skill"])

                    if SBA.Current_Game.HasAllLivePlayerDone(SLB.Current_Lobby):
                        SBA.Current_Game.OnRoundEnd()

                        SBA.Current_Game.OnRoundStart()
                        await self.broadCast(
                            BattleResultData(
                                SLB.My_Player_Info.GetId(), SBA.Current_Game
                            )
                        )

                        NewUI.PrintChatArea(
                            SBA.Current_Game.Skill_Stash.GetSkillStatus()
                        )
                        NewUI.PrintStatusArea(SBA.Current_Game.GetStatus())

                        # 判断游戏是否结束
                        lids = SBA.Current_Game.GetALiveUIDs(SLB.Current_Lobby)
                        if len(lids) <= 1:
                            if len(lids) == 1:
                                NewUI.PrintChatArea(
                                    f"游戏结束了,{SBA.Current_Game.players[lids[0]].Name}是Winner\nhost输入start再开一把"
                                )
                            else:
                                NewUI.PrintChatArea("人员全部离线，游戏结束")
                            continue
                        else:
                            if (
                                SBA.Current_Game.players[
                                    SLB.My_Player_Info.GetId()
                                ].Health
                                >= 0
                            ):
                                self.could_send_action.set()
                                NewUI.PrintChatArea("你可以发送技能了")
                                NewUI.PrintTipArea("请输出技能")
                            else:
                                NewUI.PrintTipArea("你4了，但是可以继续观战聊天")
                                NewUI.PrintChatArea("你4了，但是可以继续观战聊天")

                elif recv_data.data_type == LinkEvent.LOBBYUPDATE:
                    # 昭告全国
                    await self.broadCast(recv_data, writer)
                    SLB.Current_Lobby = recv_data.content
                    NewUI.PrintChatArea(SLB.Current_Lobby.GetLobbyTable())
                elif recv_data.data_type == LinkEvent.LOBBYASSIGN:
                    """uid用户发送了自己的name"""
                    SLB.Current_Lobby.player_infos[recv_data.uid].name = (
                        recv_data.content
                    )
                    await self.broadCast(
                        LobbyUpdateData(SLB.My_Player_Info.GetId(), SLB.Current_Lobby),
                        None,
                    )
                    NewUI.PrintChatArea(
                        SLB.Current_Lobby.GetLobbyTable().get_formatted_string()
                    )

            except ConnectionResetError:
                break

        # 用户离开
        NewUI.PrintChatArea(f"Client {addr} disconnected")
        self.clients.remove(writer)
        writer.close()
        await writer.wait_closed()
        SLB.Current_Lobby.LeavePlayer(new_player_info.GetId())
        asyncio.create_task(
            self.broadCast(
                LobbyUpdateData(SLB.My_Player_Info.GetId(), SLB.Current_Lobby),
                None,
            )
        )

    async def SendAction(self, sk: Skill):
        SBA.Current_Game.AddSkill(sk)
        NewUI.PrintTipArea(str(sk))

        if SBA.Current_Game.HasAllLivePlayerDone(SLB.Current_Lobby):
            SBA.Current_Game.OnRoundEnd()

            SBA.Current_Game.OnRoundStart()
            await self.broadCast(
                BattleResultData(SLB.My_Player_Info.GetId(), SBA.Current_Game)
            )

            NewUI.PrintChatArea(SBA.Current_Game.Skill_Stash.GetSkillStatus())
            NewUI.PrintStatusArea(SBA.Current_Game.GetStatus())

            # 判断游戏是否结束
            lids = SBA.Current_Game.GetALiveUIDs(SLB.Current_Lobby)
            if len(lids) <= 1:
                if len(lids) == 1:
                    NewUI.PrintChatArea(
                        f"游戏结束了,{SBA.Current_Game.players[lids[0]].Name}是Winner\nhost输入start再开一把"
                    )
                else:
                    NewUI.PrintChatArea("人员全部离线，游戏结束")
                return
            else:
                if SBA.Current_Game.players[SLB.My_Player_Info.GetId()].Health >= 0:
                    self.could_send_action.set()
                    NewUI.PrintChatArea("你可以发送技能了")
                    NewUI.PrintTipArea("请输出技能")
                else:
                    NewUI.PrintChatArea("你4了，但是可以继续观战聊天")
                    NewUI.PrintTipArea("你4了，但是可以继续观战聊天")

    async def SendMessage(self, msg: str):
        msg_data = MessageData(SLB.My_Player_Info.GetId(), msg)
        await self.broadCast(msg_data, None)


class ClientPlayerLink(PlayerLink):
    def __init__(self):
        super().__init__()
        self.sender = None
        self.content = None

    async def JoinLobby(self):
        """作为client加入lobby

        1. 读取配置文件的addr

        2. 尝试加入并发送测试数据包
        """
        self.host_ip = Cfg["address"]["host_ip"]
        self.port = Cfg["address"]["port"]
        NewUI.PrintChatArea("Connecting...")
        self.reader, self.writer = await asyncio.open_connection(
            self.host_ip, self.port
        )

        NewUI.PrintChatArea("Connected to server!")
        await asyncio.gather(self.recv_data(), SendThingsForever(self))

    async def Send(self, data):
        data = pickle.dumps(data)
        self.writer.write(data)
        await self.writer.drain()

    async def SendAction(self, sk: Skill):
        NewUI.PrintTipArea(str(sk))
        await self.Send(BattleActionData(SLB.My_Player_Info.GetId(), sk))

    async def SendMessage(self, msg: str):
        await self.Send(MessageData(SLB.My_Player_Info.GetId(), msg))

    async def recv_data(self):
        global TimesToReconnect
        TimesToReconnect = 5
        while True:
            try:
                data = []
                while not self.reader.at_eof():
                    try:
                        packet = await asyncio.wait_for(
                            self.reader.read(4096), timeout=0.5
                        )
                        if not packet:
                            NewUI.PrintChatArea("Server disconnected")
                            break
                        data.append(packet)
                    except asyncio.TimeoutError:
                        break

                if len(data) == 0:
                    continue

                recv_data: LinkData = pickle.loads(b"".join(data))
                parserd_data = recv_data.Parser()
                # 根据messageEvent来分支
                if recv_data.data_type == LinkEvent.CHATMESSAGE:
                    NewUI.PrintChatArea(
                        f"{recv_data.uid}/{SLB.Current_Lobby.player_infos[recv_data.uid].GetName()}:"
                        + parserd_data["msg"]
                    )

                elif recv_data.data_type == LinkEvent.BATTLERESULT:
                    SBA.Current_Game = parserd_data["game"]
                    NewUI.PrintChatArea(SBA.Current_Game.Skill_Stash.GetSkillStatus())
                    NewUI.PrintStatusArea(SBA.Current_Game.GetStatus())
                    # 判断游戏是否结束
                    lids = SBA.Current_Game.GetALiveUIDs(SLB.Current_Lobby)
                    if len(lids) <= 1:
                        if len(lids) == 1:
                            NewUI.PrintChatArea(
                                f"游戏结束了,{SBA.Current_Game.players[lids[0]].Name}是Winner\nhost输入start再开一把"
                            )
                        else:
                            NewUI.PrintChatArea("人员全部离线，游戏结束")
                    else:
                        if (
                            SBA.Current_Game.players[SLB.My_Player_Info.GetId()].Health
                            >= 0
                        ):
                            self.could_send_action.set()
                            # NewUI.PrintTipArea("准")
                            NewUI.PrintChatArea("你可以发送技能了")
                            NewUI.PrintTipArea("请输入技能")
                        else:
                            NewUI.PrintTipArea("你4了，但是可以继续观战聊天")
                            NewUI.PrintChatArea("你4了，但是可以继续观战聊天")

                elif recv_data.data_type == LinkEvent.LOBBYUPDATE:
                    SLB.Current_Lobby = recv_data.content
                    NewUI.PrintChatArea(
                        SLB.Current_Lobby.GetLobbyTable().get_formatted_string()
                    )

                elif recv_data.data_type == LinkEvent.LOBBYASSIGN:
                    """被分配id"""
                    SLB.My_Player_Info.id = parserd_data["value"]
                    SLB.My_Player_Info.name = Cfg["player_info"]["player_name"]
                    await self.Send(
                        LobbyAssignData(SLB.My_Player_Info.id, SLB.My_Player_Info.name)
                    )
                elif recv_data.data_type == LinkEvent.BATTLESTART:
                    SBA.Current_Game = recv_data.content
                    NewUI.PrintStatusArea(SBA.Current_Game.GetStatus())
                    self.could_send_action.set()
                    NewUI.PrintTipArea("请输出技能")
                    NewUI.PrintChatArea("你可以使用技能了")

            except (ConnectionResetError, EOFError, pickle.UnpicklingError):
                NewUI.PrintChatArea("Server disconnected")

                ok = False
                while TimesToReconnect > 0:
                    TimesToReconnect -= 1
                    try:
                        self.reader, self.writer = await asyncio.open_connection(
                            self.host_ip, self.port
                        )
                        ok = True
                        break
                    except BaseException as e:
                        NewUI.PrintChatArea(str(e))

                if ok:
                    continue
                else:
                    break


"""设置状态"""


"""通用的utils"""


async def SendRaw():
    """发送数据包"""
    ...


async def SendThingsForever(Linker: PlayerLink):
    loop = asyncio.get_running_loop()
    while True:
        await Linker.could_type.wait()
        content = await ReadInput()  # vanilla input
        if content is None or len(content) == 0:
            continue
        if content[0] == "!":
            # 发送message
            asyncio.create_task(Linker.SendMessage(content[1:]))
            continue
        elif (await LM.RunMenuCommand(content, Linker)) is True:
            # 执行了菜单指令
            continue
        else:
            # action
            if Linker.could_send_action.is_set() is False:
                # 现在不能发送action
                NewUI.PrintChatArea("It is not right time to send action")
                continue
            else:
                # parser first
                ok, msg, sk = ParserSkill(
                    SLB.My_Player_Info.GetId(), content, SBA.Current_Game
                )
                if ok is False or sk is None:
                    NewUI.PrintChatArea("Fail:" + msg)
                    continue
                else:
                    # sendaction
                    asyncio.create_task(Linker.SendAction(sk))
                    # 禁用
                    Linker.could_send_action.clear()
                    # t.add_done_callback()
                    ...

                # ~ 时间到了也禁用
                # 最后发送


# def SendActionCalback(obj):
#     print()
