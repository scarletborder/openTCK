from typing import TYPE_CHECKING

from src.constant.enum.battle_trigger import TriggerType
from src.models.battle.skill import Skill, SkillID

if TYPE_CHECKING:
    from src.models.battle.game import Game
    from src.models.battle.skill import Skill
    from src.constant.enum.battle_trigger import TriggerType

"""触发器
每个触发器在实例化时，需要传入Skill自己作为成员

在被触发时



"""


class BattleTrigger:
    def __init__(self, game: "Game", tri_type: "TriggerType", sk: "Skill"):
        self.Type = tri_type
        self.Original_Skill = sk
        self.context = {}

    def Cast(self, game: "Game", *arg):
        """触发器触发时的函数

        固定接受参数包括game，还接受其他可能的参数，如特定技能触发器会传入引发触发器的技能实例
        """
        ...

    @staticmethod
    def NewTrigger(game: "Game", sk: "Skill", args) -> "BattleTrigger": ...


class SpecifiedSkillTrigger(BattleTrigger):
    def __init__(
        self, game: "Game", tri_type: TriggerType, sk: Skill, sp_skid: SkillID
    ):
        super().__init__(game, tri_type, sk)
        self.sp_skid = sp_skid

    def Cast(self, game: "Game", sk: Skill):
        """指定技能触发器触发时的函数

        固定接受参数包括game，和引发触发器的技能实例
        """
        ...


class SpecifiedPlayerTrigger(BattleTrigger):
    def __init__(self, game: "Game", tri_type: TriggerType, sk: Skill, sp_plid: int):
        super().__init__(game, tri_type, sk)
        self.sp_plid = sp_plid

    def Cast(self, game: "Game", sk: Skill):
        """指定技能触发器触发时的函数

        固定接受参数包括game，和引发触发器的技能实例
        """
        ...

class SpecifiedTargetTrigger(BattleTrigger):
    def __init__(
        self, game: "Game", tri_type: TriggerType, sk: Skill, sp_tid: int
    ):
        super().__init__(game, tri_type, sk)
        self.sp_tid = sp_tid

    def Cast(self, game: "Game", sk: Skill):
        ...


class ChangePointTrigger(BattleTrigger):

    def __init__(self, game: "Game", tri_type: TriggerType, sk: Skill, sp_plid: int):
        super().__init__(game, tri_type, sk)
        self.sp_plid = sp_plid

    def Cast(self, game: "Game", sk: Skill, uid: int, change: list[int]):
        """数值变动（血量和点数）

        sk - 造成影响的技能技能,对于trigger造成的，是original_skill
        """
        ...
