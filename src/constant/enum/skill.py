from enum import Enum


def int_to_enum(value, enum_class, default=None):
    """根据枚举类的名字返回枚举量
    @param: int - 常量值
    @param: enum_class - 类的名字
    """
    try:
        return enum_class(value)
    except ValueError:
        return default


class SkillType(Enum):
    SINGLE = 0x01
    MULTI = 0x02
    DEFENSE = 0x04
    COMMAND = 0x08


class SkillID(Enum):
    # single
    SHA = 1
    QIN = 2
    FAGONG = 3
    XIXUE = 4
    JUESHA = 6

    # multi
    WANJIAN = 101
    NANMAN = 102
    LEIDIAN = 103
    HUOWU = 104

    # defense
    FANGYU = 201
    GAOFANG = 202

    # command
    SLEEP = 300
    JIDIAN = 301
    XDANG = 302
    DUX = 303
    BAOLI = 304
    CHU = 305
    XIADU = 307
    JIU = 310
    ZISHA = 324
    TAO = 329
    SHANDIAN = 333
    HUDUN = 343
    FANTAN = 346
