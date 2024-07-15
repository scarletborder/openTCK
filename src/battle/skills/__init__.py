import threading
from src.models.battle.skill import Skill

Skill_Table: dict[int, type[Skill]] = dict()  # 技能id - 技能
Skill_Name_To_ID: dict[str, int] = dict()  # 技能名 - 技能id


class Once:
    def __init__(self):
        self._lock = threading.Lock()
        self._has_run = False

    def do(self, func, *args, **kwargs):
        with self._lock:
            if not self._has_run:
                self._has_run = True
                func(*args, **kwargs)


# 示例函数
def ImportSkillTable():
    import src.battle.skills.skill_table


# # 创建 Once 实例
once = Once()
once.do(ImportSkillTable)
