from src.constant.enum.skill import SkillID
from src.constant.enum.battle_tag import TagEvent

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.game import Game, Skill
    from src.models.battle.player import Player


def GetPlayerTags(player: "Player") -> str:
    ret = []
    for tag_eve, number in player.tag.items():
        if number == 0:
            continue
        ret.append(f"{tag_eve.name} {number}")
    return "|".join(ret)
