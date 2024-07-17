from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.battle.skill import CommandSkill

Cmd_Skill_Queue = ["baoli", "xiadu", "fantan", "jiu", "tao", "jidian"]


def GetCMDQueue(cskl: list["CommandSkill"]) -> list["CommandSkill"]:
    # 构建一个字典来快速查找字符串在 string_list 中的索引
    index_map = {id_str: index for index, id_str in enumerate(Cmd_Skill_Queue)}

    # 根据字符串列表排序对象列表
    cskl.sort(key=lambda obj: index_map[obj.GetName()])
    return cskl
