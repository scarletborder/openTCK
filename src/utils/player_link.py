from abc import ABC, abstractmethod
import asyncio


class PlayerLink(ABC):
    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    def JoinLobby(self): ...

    @abstractmethod
    def SendSkills(self, skills: list): ...

    @abstractmethod
    def SendMessage(self, msg: list): ...


class HostPlayerLink(PlayerLink):
    def __init__(self):
        self.a = 0

    def JoinLobby(self):
        """作为host加入lobby

        1. 读取配置文件中的开放ip和port

        2. 尝试开放
        """
        ...

    def SendSkills(self, skills: list): ...

    def SendMessage(self, msg: list): ...


class ClientPlayerLink(PlayerLink):
    def __init__(self): ...

    def JoinLobby(self):
        """作为client加入lobby

        1. 读取配置文件的addr

        2. 尝试加入并发送测试数据包
        """
        ...

    def SendSkills(self, skills: list): ...

    def SendMessage(self, msg: list): ...


"""通用的utils"""


def SendRaw():
    """发送数据包"""
    ...
