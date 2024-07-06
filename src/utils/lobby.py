from prettytable import PrettyTable


class PlayerInfo:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        pass

    def GetIDWithName(self) -> tuple[int, str]:
        return (self.id, self.name)

    def GetName(self) -> str:
        return self.name

    def GetId(self) -> int:
        return self.id


class Lobby:
    def __init__(self) -> None:
        self.plyer_infos: list[PlayerInfo] = []

    def AddPlayer(self, name: str):
        current_number = len(self.plyer_infos)
        new_player = PlayerInfo(current_number + 1, name)
        self.plyer_infos.append(new_player)

    def GetGameArgs(self) -> list[tuple[int, str]]:
        """获得启动游戏需要的参数"""
        ret: list[tuple[int, str]] = []
        for p in self.plyer_infos:
            ret.append((p.GetId(), p.GetName()))

        return ret

    # 显示类
    def GetLobbyTable(self) -> PrettyTable:
        table = PrettyTable()
        table.field_names = ["id", "name"]
        for p in self.plyer_infos:
            table.add_row([f"{p.GetId()}", f"{p.GetName()}"])

        return table
