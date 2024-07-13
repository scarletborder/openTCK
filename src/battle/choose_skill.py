from src.battle.skills import Skill_Table, Skill_Name_To_ID
from src.models.battle.game import Game
from src.models.battle.skill import Skill


def ChooseSkillById(
    caster_id: int, skill_id: int, args: list[str], game: Game
) -> tuple[bool, str, Skill | None]:
    if skill_id not in Skill_Table.keys():
        return False, "该技能id不存在", None

    ok, sk, msg = Skill_Table[skill_id].NewSkill(caster_id, args)
    if ok is False or sk is None:
        return False, msg, None
    return *game.JudgeAddSkill(sk), sk


def ChooseSkillByName(
    caster_id: int, skill_name: str, args: list[str], game: Game
) -> tuple[bool, str, Skill | None]:
    if skill_name not in Skill_Name_To_ID.keys():
        return False, "该技能名不存在", None

    return ChooseSkillById(caster_id, Skill_Name_To_ID[skill_name], args, game)


def ParserSkill(
    caster_id: int, input_s: str, game: "Game"
) -> tuple[bool, str, "Skill | None"]:
    """解析用户输入内容为技能或者提示输入不合法或当前情况无法使用
    @input_s : 用户输入的原生内容，会被解析成skill供返回
    """
    sl = input_s.strip().split(" ")
    if len(sl) == 0:
        return False, "未识别到任何技能", None

    try:
        sid = int(sl[0])
    except ValueError:
        sid = -1

    if sid < 0:
        return ChooseSkillByName(caster_id, sl[0], sl[1:], game)
    else:
        return ChooseSkillById(caster_id, sid, sl[1:], game)
