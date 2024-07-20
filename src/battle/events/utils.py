from src.constant.enum.skill import SkillID
from src.constant.enum.battle_tag import TagEvent

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game, Skill


def CheckPlayerTagEvent(game: "Game", uid: int, timing: int):
    """为某名玩家判定和触发TagEvent效果"""

    if timing == 1:
        if game.players[uid].tag.get(TagEvent.SHANDIAN, 0):
            if game.Skill_Used_Times.get(SkillID.XIADU, 0) >= 3:
                game.players[uid].InstantKill(game)
                game.players[uid].tag[TagEvent.SHANDIAN] = 0

    if timing == 4:
        if game.players[uid].is_hurt:
            if game.players[uid].tag.get(TagEvent.HUDUN, 0):
                game.players[uid].tag[TagEvent.HUDUN] -= 1


def AlterTagEvent(game: "Game"):
    """对TagEvent的归属进行改动"""
    live_uids = game.GetLiveUIDs()
    num_players = len(live_uids)

    if num_players == 0:
        return

    # 创建一个列表来记录拥有 SHANDIAN 标签的玩家索引
    shandian_indices = []

    for i in range(num_players):
        if game.players[live_uids[i]].tag.get(TagEvent.SHANDIAN):
            shandian_indices.append(i)

    # 遍历所有拥有 SHANDIAN 标签的玩家并将其传递给下一个玩家
    for i in shandian_indices:
        current_player = game.players[live_uids[i]]
        current_player.tag[TagEvent.SHANDIAN] = 0
        next_player = game.players[live_uids[(i + 1) % num_players]]
        next_player.tag[TagEvent.SHANDIAN] = 1

def InitializeTagEvent(game: "Game"):
    """初始化TagEvent"""

    AlterTagEvent(game)

def PlayerCanBeHurt(game: "Game", player_id: int):
    if game.players[player_id].tag.get(TagEvent.HUDUN, 0):
        return False
    else:
        return True
    