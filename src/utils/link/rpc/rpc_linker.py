from abc import ABC, abstractmethod
from src.models.battle.skill import Skill


class RpcLinker(ABC):
    @abstractmethod
    @staticmethod
    async def SendAction(s: str, sk: Skill): ...

    @abstractmethod
    @staticmethod
    async def SendMessage(s: str): ...
