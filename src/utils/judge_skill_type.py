from src.constant.enum.skill import SkillID


def IsSingle(s: SkillID) -> bool:
    return 0 <= s.value < 100


def IsMulti(s: SkillID) -> bool:
    return 100 <= s.value < 200


def IsDefense(s: SkillID) -> bool:
    return 200 <= s.value < 300


def IsCommand(s: SkillID) -> bool:
    return 300 <= s.value < 400


def IsSingleByInt(s: int) -> bool:
    return 0 <= s < 100


def IsMultiByInt(s: int) -> bool:
    return 100 <= s < 200


def IsDefenseByInt(s: int) -> bool:
    return 200 <= s < 300


def IsCommandByInt(s: int) -> bool:
    return 300 <= s < 400
