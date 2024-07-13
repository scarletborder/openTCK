from abc import ABC, abstractmethod
from src.battle.choose_skill import ParserSkill
from src.models.link.link_data import (
    LinkData,
    MessageData,
    BattleActionData,
    BattleResultData,
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
        self.could_send_action.set()
        self.is_host = False

    @abstractmethod
    async def JoinLobby(self): ...

    @abstractmethod
    async def SendAction(self, skill: Skill): ...

    @abstractmethod
    async def SendMessage(self, msg: str): ...


class HostPlayerLink(PlayerLink):
    def __init__(self):
        self.clients = []

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

    async def handle_client(self, reader, writer):
        self.clients.append(writer)
        addr = writer.get_extra_info("peername")
        print(f"New client: {addr}")

        while True:
            try:
                data = await reader.read(4096)
                if not data:
                    break

                recv_data: LinkData = pickle.loads(data)
                parserd_data = recv_data.Parser()
                # 根据messageEvent来分支
                if recv_data.data_type == LinkEvent.CHATMESSAGE:
                    print(parserd_data["msg"])
                    asyncio.create_task(self.broadCast(recv_data, writer))

                elif recv_data.data_type == LinkEvent.BATTLEACTION:
                    # 加入技能
                    SBA.Current_Game.AddSkill(parserd_data["skill"])

                    if (
                        len(SBA.Current_Game.Skill_Stash.caster_skill)
                        >= SLB.Current_Lobby.GetNumber()
                    ):  # 如果所有人都做出了行为
                        SBA.Current_Game.OnRoundEnd()
                        asyncio.create_task(
                            self.broadCast(
                                BattleResultData(
                                    SLB.My_Player_Info.GetId(), SBA.Current_Game
                                )
                            )
                        )
                    ...

                    ...
                elif recv_data.data_type == LinkEvent.LOBBYUPDATE:
                    SLB.Current_Lobby = recv_data.content
                    asyncio.create_task(self.broadCast(recv_data, writer))

            except ConnectionResetError:
                break

        print(f"Client {addr} disconnected")
        self.clients.remove(writer)
        writer.close()
        await writer.wait_closed()

    async def SendAction(self, sk: Skill):
        # 禁用
        self.could_send_action.clear()
        SBA.Current_Game.AddSkill(sk)

        if (
            len(SBA.Current_Game.Skill_Stash.caster_skill)
            >= SLB.Current_Lobby.GetNumber()
        ):  # 如果所有人都做出了行为
            SBA.Current_Game.OnRoundEnd()
            asyncio.create_task(
                self.broadCast(
                    BattleResultData(SLB.My_Player_Info.GetId(), SBA.Current_Game)
                )
            )

    async def SendMessage(self, msg: str):
        msg_data = MessageData(SLB.My_Player_Info.GetId(), msg)
        asyncio.create_task(self.broadCast(msg_data, None))


class ClientPlayerLink(PlayerLink):
    def __init__(self): ...

    async def JoinLobby(self):
        """作为client加入lobby

        1. 读取配置文件的addr

        2. 尝试加入并发送测试数据包
        """
        ...

    async def SendAction(self, skills: list): ...

    async def SendMessage(self, msg: str): ...


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
        if content[0] == "!":
            # 发送message
            asyncio.create_task(Linker.SendMessage(content[1:]))
            continue
        elif LM.IsMenuCommand(content) is True:
            # 执行菜单指令
            ...
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
                    # t.add_done_callback()
                    ...

                # ~ 时间到了也禁用
                # 最后发送


# def SendActionCalback(obj):
#     print()
