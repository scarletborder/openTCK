from src.models.battle.game import Game
from src.models.battle.player import Player


def CreateNewGame(id_name: list[tuple[int, str]]) -> Game:
    new_game = Game()
    for t_id_name in id_name:
        new_player = Player(t_id_name[1], t_id_name[0])
        new_game.AddPlayer(new_player)

    return new_game
