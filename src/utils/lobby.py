from prettytable import PrettyTable
import src.utils.link.stub.common_pb2 as copb2


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
        self.lack: "list[int]" = []

    @staticmethod
    def NewFromPb2(pb2: copb2.LobbyStatus) -> "Lobby":
        ret = Lobby()
        players: list[tuple[int, str, bool]] = []
        for player in pb2.players:
            players.append((player.uid, player.name, player.is_leave))
        players = sorted(players, key=lambda x: x[0])

        for player in players:
            ret.player_infos.append(PlayerInfo(player[0], player[1]))
            if player[2]:
                ret.lack.append(player[0])
        return ret

    def GetNumber(self):
        """获取大厅在线人数(不包括离开人数)"""
        return len(self.player_infos) - len(self.lack)

    def AddPlayer(self, name: str = "Anonymous") -> PlayerInfo:
        # 现在不再填lack的坑,只有当name相同时才填
        for uid in self.lack:
            if self.player_infos[uid].name == name:
                # 占坑
                ret = PlayerInfo(uid, name)
                self.player_infos[uid] = ret
                self.lack.remove(uid)
                return ret

        # 如果全部不匹配,说明新玩家
        new_uid = len(self.player_infos)
        new_player = PlayerInfo(new_uid, name)
        self.player_infos.append(new_player)
        return new_player

    def IsUidLeave(self, uid: int) -> bool:
        """指定uid用户是否离开"""
        return uid in self.lack

    def GetGameArgs(self) -> list[tuple[int, str]]:
        """获得启动游戏需要的参数"""
        ret: list[tuple[int, str]] = []
        for p in self.player_infos:
            ret.append((p.GetId(), p.GetName()))

        return ret

    def LeavePlayer(self, uid: int):
        """一位玩家离开"""
        self.lack.append(uid)
        self.player_infos[uid].name = "LEAVE " + self.player_infos[uid].name

    # 显示类
    def GetLobbyTable(self) -> PrettyTable:
        table = PrettyTable()
        table.field_names = ["id", "name"]
        for p in self.player_infos:
            table.add_row([f"{p.GetId()}", f"{p.GetName()}"])

        return table
