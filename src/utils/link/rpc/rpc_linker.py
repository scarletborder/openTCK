from abc import ABC, abstractmethod
from src.models.battle.skill import Skill


class RpcLinker(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.is_host = False

    @abstractmethod
    async def SendAction(self, sk_str: str, sk: Skill): ...

    @abstractmethod
    async def SendMessage(self, s: str): ...

    @abstractmethod
    async def JoinLobby(self): ...
