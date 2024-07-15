import tomlkit
from tomlkit import TOMLDocument

# from src.utils.pkui.global_utils import NewUI

Cfg = {}


with open("src/constant/config/config.toml", "r", encoding="utf-8") as file:
    # 读取 TOML 文件
    Cfg = tomlkit.parse(file.read())


def ReadComment(father: str, setting: str) -> str:
    """获取指定项目的注释"""
    comments = None
    if father not in Cfg:
        return f"No such father option '{father}'"

    if setting not in Cfg[father]:
        return f"No such option '{setting}'"

    comments = Cfg[father][setting].trivia.comment

    if comments:
        return comments
    else:
        return f"No comments found before the key '{setting}'."


# # 访问 TOML 文件中的数据
# player_name = config["player_info"]["player_name"]
# host_ip = config["address"]["host_ip"]
# port = config["address"]["port"]
