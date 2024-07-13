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
        self.player_infos: list[PlayerInfo] = []
        self.lack = []

    def GetNumber(self):
        return len(self.player_infos) - len(self.lack)

    def AddPlayer(self, name: str) -> PlayerInfo:
        # 如果lack还有坑，填补上
        if len(self.lack) > 0:
            new_uid = self.lack[0]
            self.lack = self.lack[1:]
            new_player = PlayerInfo(new_uid, name)
            self.player_infos[new_uid] = new_player
        else:
            new_uid = len(self.player_infos) + 1
            new_player = PlayerInfo(new_uid, name)
            self.player_infos.append(new_player)

        return new_player

    def GetGameArgs(self) -> list[tuple[int, str]]:
        """获得启动游戏需要的参数"""
        ret: list[tuple[int, str]] = []
        for p in self.player_infos:
            ret.append((p.GetId(), p.GetName()))

        return ret

    def LeavePlayer(self, uid: int):
        """一位玩家离开"""
        self.lack.append(uid)

    # 显示类
    def GetLobbyTable(self) -> PrettyTable:
        table = PrettyTable()
        table.field_names = ["id", "name"]
        for p in self.player_infos:
            table.add_row([f"{p.GetId()}", f"{p.GetName()}"])

        return table
