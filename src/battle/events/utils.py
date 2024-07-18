from src.constant.enum.skill import SkillID
from src.constant.enum.battle_tag import TagEvent

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game


def CheckPlayerTagEvent(game: "Game", uid: int):
    """为某名玩家判定和触发TagEvent效果"""
    if game.players[uid].tag.get(TagEvent.SHANDIAN, 0):
        if game.Skill_Used_Times.get(SkillID.XIADU, 0) >= 3:
            game.players[uid].InstantKill()
            game.players[uid].tag[TagEvent.SHANDIAN] = 0


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
