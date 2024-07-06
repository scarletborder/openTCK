from src.models.battle.player import Player
from prettytable import PrettyTable


class Game:
    def __init__(self):
        self.players: dict[int, Player] = {}

    def AddPlayer(self, player: Player):
        self.players[player.id] = player

    def GetStatus(self) -> PrettyTable:
        """展示场上每个玩家的属性"""
        table = PrettyTable()
        table.field_names = ["id", "name", "Health", "Point"]
        for t_id, t_player in self.players.items():
            table.add_row(
                [
                    f"{t_id}",
                    f"{t_player.Name}",
                    f"{t_player.Health}",
                    f"{t_player.Point}",
                ]
            )

        return table
