from src.battle.skills import Skill_Table, Skill_Name_To_ID
from src.models.battle.game import Game


def ChooseSkillById(
    caster_id: int, target_id: int, times: int, skill_id: int, game: Game
) -> tuple[bool, str]:
    if skill_id not in Skill_Table.keys():
        return False, "该技能id不存在"

    return game.AddSkill(caster_id, target_id, times, skill_id)


def ChooseSkillByName(
    caster_id: int, target_id: int, times: int, skill_name: str, game: Game
) -> tuple[bool, str]:
    if skill_name not in Skill_Name_To_ID.keys():
        return False, "该技能名不存在"

    return ChooseSkillById(
        caster_id, target_id, times, Skill_Name_To_ID[skill_name], game
    )
