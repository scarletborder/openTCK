from enum import Enum

class SkillModifiedInfo(Enum):
    EXTRA_DAMAGE = 1 # attr: extra_damage
    INVALIDATED = 2 # attr: (caster_id, target_idd)