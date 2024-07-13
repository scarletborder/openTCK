from abc import ABC, abstractmethod
from src.battle.choose_skill import ParserSkill
from src.battle.new_game import Game, Player
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
        print(f"Serving on {addr}")

        self.could_type.set()
        self.could_send_action.clear()

        # gather forever
        async with self.Server:
            await asyncio.gather(self.Server.serve_forever(), SendThingsForever(self))

        print("大厅已经关闭")

    async def StartGame(self):
        SBA.Current_Game = Game()
        args = SLB.Current_Lobby.GetGameArgs()
        for uid, pname in args:
            SBA.Current_Game.AddPlayer(Player(pname, uid))

        await self.broadCast(
            BattleStartData(SLB.My_Player_Info.GetId(), SBA.Current_Game)
        )

        print(SBA.Current_Game.GetStatus())
        SBA.Current_Game.OnRoundStart()
        self.could_send_action.set()
        print("你可以发送技能了")

    async def handle_client(self, reader, writer):
        self.clients.append(writer)
        addr = writer.get_extra_info("peername")
        print(f"New client: {addr}")
        # 分配一个player_info
        new_player_info = SLB.Current_Lobby.AddPlayer()
        writer.write(
            pickle.dumps(
                LobbyAssignData(SLB.My_Player_Info.GetId(), new_player_info.GetId())
            )
        )
        await writer.drain()

        while True:
            try:
                data = await reader.read(4096)
                if not data:
                    break

                recv_data: LinkData = pickle.loads(data)
                parserd_data = recv_data.Parser()
                # 根据messageEvent来分支
                if recv_data.data_type == LinkEvent.CHATMESSAGE:
                    print(
                        f"{recv_data.uid}/{SLB.Current_Lobby.player_infos[recv_data.uid].GetName()}:"
                        + parserd_data["msg"]
                    )

                    await self.broadCast(recv_data, writer)

                elif recv_data.data_type == LinkEvent.BATTLEACTION:
                    # 加入技能
                    SBA.Current_Game.AddSkill(parserd_data["skill"])

                    if SBA.Current_Game.HasAllLivePlayerDone(SLB.Current_Lobby):
                        SBA.Current_Game.OnRoundEnd()
                        await self.broadCast(
                            BattleResultData(
                                SLB.My_Player_Info.GetId(), SBA.Current_Game
                            )
                        )

                        print(SBA.Current_Game.Skill_Stash.GetSkillStatus())
                        print(SBA.Current_Game.GetStatus())
                        SBA.Current_Game.OnRoundStart()
                        # 判断游戏是否结束
                        lids = SBA.Current_Game.GetALiveUIDs(SLB.Current_Lobby)
                        if len(lids) <= 1:
                            if len(lids) == 1:
                                print(
                                    f"游戏结束了,{SBA.Current_Game.players[lids[0]].Name}是Winner\nhost输入start再开一把"
                                )
                            else:
                                print("人员全部离线，游戏结束")
                            continue
                        else:
                            if (
                                SBA.Current_Game.players[
                                    SLB.My_Player_Info.GetId()
                                ].Health
                                > 0
                            ):
                                self.could_send_action.set()
                                print("你可以发送技能了")
                            else:
                                print("你4了，但是可以继续观战聊天")

                elif recv_data.data_type == LinkEvent.LOBBYUPDATE:
                    # 昭告全国
                    await self.broadCast(recv_data, writer)
                    SLB.Current_Lobby = recv_data.content
                    print(SLB.Current_Lobby.GetLobbyTable())
                elif recv_data.data_type == LinkEvent.LOBBYASSIGN:
                    """uid用户发送了自己的name"""
                    SLB.Current_Lobby.player_infos[recv_data.uid].name = (
                        recv_data.content
                    )
                    await self.broadCast(
                        LobbyUpdateData(SLB.My_Player_Info.GetId(), SLB.Current_Lobby),
                        None,
                    )
                    print(SLB.Current_Lobby.GetLobbyTable())

            except ConnectionResetError:
                break

        # 用户离开
        print(f"Client {addr} disconnected")
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

        if SBA.Current_Game.HasAllLivePlayerDone(SLB.Current_Lobby):
            SBA.Current_Game.OnRoundEnd()
            await self.broadCast(
                BattleResultData(SLB.My_Player_Info.GetId(), SBA.Current_Game)
            )

            print(SBA.Current_Game.Skill_Stash.GetSkillStatus())
            print(SBA.Current_Game.GetStatus())
            SBA.Current_Game.OnRoundStart()
            # 判断游戏是否结束
            lids = SBA.Current_Game.GetALiveUIDs(SLB.Current_Lobby)
            if len(lids) <= 1:
                if len(lids) == 1:
                    print(
                        f"游戏结束了,{SBA.Current_Game.players[lids[0]].Name}是Winner\nhost输入start再开一把"
                    )
                else:
                    print("人员全部离线，游戏结束")
                return
            else:
                if SBA.Current_Game.players[SLB.My_Player_Info.GetId()].Health > 0:
                    self.could_send_action.set()
                    print("你可以发送技能了")
                else:
                    print("你4了，但是可以继续观战聊天")

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
        print("Connecting...")
        self.reader, self.writer = await asyncio.open_connection(
            self.host_ip, self.port
        )

        print("Connected to server!")
        await asyncio.gather(
            self.recv_data(self.reader, self.writer), SendThingsForever(self)
        )

    async def Send(self, data):
        data = pickle.dumps(data)
        self.writer.write(data)
        await self.writer.drain()

    async def SendAction(self, sk: Skill):
        await self.Send(BattleActionData(SLB.My_Player_Info.GetId(), sk))

    async def SendMessage(self, msg: str):
        await self.Send(MessageData(SLB.My_Player_Info.GetId(), msg))

    async def recv_data(self, reader, writer):
        while True:
            try:
                data = await reader.read(4096)
                if not data:
                    print("Server disconnected")
                    break

                recv_data: LinkData = pickle.loads(data)
                parserd_data = recv_data.Parser()
                # 根据messageEvent来分支
                if recv_data.data_type == LinkEvent.CHATMESSAGE:
                    print(
                        f"{recv_data.uid}/{SLB.Current_Lobby.player_infos[recv_data.uid].GetName()}:"
                        + parserd_data["msg"]
                    )

                elif recv_data.data_type == LinkEvent.BATTLERESULT:
                    SBA.Current_Game = parserd_data["game"]
                    print(SBA.Current_Game.Skill_Stash.GetSkillStatus())
                    print(SBA.Current_Game.GetStatus())
                    # 判断游戏是否结束
                    lids = SBA.Current_Game.GetALiveUIDs(SLB.Current_Lobby)
                    if len(lids) <= 1:
                        if len(lids) == 1:
                            print(
                                f"游戏结束了,{SBA.Current_Game.players[lids[0]].Name}是Winner\nhost输入start再开一把"
                            )
                        else:
                            print("人员全部离线，游戏结束")
                    else:
                        if (
                            SBA.Current_Game.players[SLB.My_Player_Info.GetId()].Health
                            > 0
                        ):
                            self.could_send_action.set()
                            print("你可以发送技能了")
                        else:
                            print("你4了，但是可以继续观战聊天")

                elif recv_data.data_type == LinkEvent.LOBBYUPDATE:
                    SLB.Current_Lobby = recv_data.content
                    print(SLB.Current_Lobby.GetLobbyTable())

                elif recv_data.data_type == LinkEvent.LOBBYASSIGN:
                    """被分配id"""
                    SLB.My_Player_Info.id = parserd_data["value"]
                    SLB.My_Player_Info.name = Cfg["player_info"]["player_name"]
                    await self.Send(
                        LobbyAssignData(SLB.My_Player_Info.id, SLB.My_Player_Info.name)
                    )
                elif recv_data.data_type == LinkEvent.BATTLESTART:
                    SBA.Current_Game = recv_data.content
                    print(SBA.Current_Game.GetStatus())
                    self.could_send_action.set()
                    print("你可以使用技能了")

            except (ConnectionResetError, EOFError, pickle.UnpicklingError):
                print("Server disconnected")
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
        content = await loop.run_in_executor(None, input, ">")  # vanilla input
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
                print("It is not right time to send action")
                continue
            else:
                # parser first
                ok, msg, sk = ParserSkill(
                    SLB.My_Player_Info.GetId(), content, SBA.Current_Game
                )
                if ok is False or sk is None:
                    print("Fail:" + msg)
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
