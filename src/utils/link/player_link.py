from abc import ABC, abstractmethod
from src.utils.parser_action import ParserSkillList
from src.models.link.link_data import (
    LinkData,
    MessageData,
    BattleActionData,
    BattleResultData,
    LinkEvent,
)
from src.constant.config.conf import Cfg
import src.utils.link.link_menu as LM
import asyncio
import pickle


class PlayerLink(ABC):
    @abstractmethod
    def __init__(self):
        self.could_type = asyncio.Event()  # 是否可以输入字符
        self.could_send_action = asyncio.Event()  # 是否可以出招

    @abstractmethod
    async def JoinLobby(self): ...

    @abstractmethod
    async def SendAction(self, skills: list): ...

    @abstractmethod
    async def SendMessage(self, msg: str): ...


class HostPlayerLink(PlayerLink):
    def __init__(self):
        self.clients = []

    async def JoinLobby(self):
        """作为host创建lobby

        1. 读取配置文件中的开放ip和port

        2. 尝试开放
        """
        self.Player_Name = Cfg["player_info"]["player_name"]
        self.host_ip = Cfg["address"]["host_ip"]
        self.port = Cfg["address"]["port"]
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
        ...

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
                    print()
                    for client in self.clients:
                        if client != writer:
                            client.write(data)
                            await client.drain()

                elif recv_data.data_type == LinkEvent.BATTLEACTION:
                    if self.could_send_action.is_set() is False:
                        # 忽略
                        ...
                    ...

                if message.strip() == "!":
                    break
                print(f"Received {message} from {addr}")
                await broadcast(message, writer)
            except ConnectionResetError:
                break

        print(f"Client {addr} disconnected")
        self.clients.remove(writer)
        writer.close()
        await writer.wait_closed()

    async def SendAction(self, skills: list): ...

    async def SendMessage(self, msg: list): ...


class ClientPlayerLink(PlayerLink):
    def __init__(self): ...

    async def JoinLobby(self):
        """作为client加入lobby

        1. 读取配置文件的addr

        2. 尝试加入并发送测试数据包
        """
        ...

    async def SendAction(self, skills: list): ...

    async def SendMessage(self, msg: list): ...


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
                ok, skill_list = ParserSkillList(content)
                if ok is False:
                    print("Your action input is not legal")
                    continue
                # judge 能不能放出来

                # 最后发送
                Linker.SendAction()
