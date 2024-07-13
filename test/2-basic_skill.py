"""
test02
测试最基本的杀，qin，法攻, 几种防御对game的影响

game的技能stash对health change的影响

同时测试一些非法的情景，涉及
1. 不存在的技能
2. 非法的连段
3. point不足情况下的释放
"""

# src/test/test_main.py
import sys
import os

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录
project_root = os.path.abspath(os.path.join(current_dir, "../"))

# 将项目根目录添加到 sys.path
sys.path.append(project_root)

from src.utils.lobby import Lobby
import src.battle.new_game as ng

example_lobby = Lobby()
example_lobby.AddPlayer("Dreamfish")
example_lobby.AddPlayer("Turbo")
example_lobby.AddPlayer("DHLZero")

print("测试大厅中的显示")
lobby_table = example_lobby.GetLobbyTable()
print(lobby_table)

print("游戏内部的显示")
game = ng.CreateNewGame(example_lobby.GetGameArgs())
print(game.GetStatus())


print("#" * 20)
print("技能测试")
import src.battle.choose_skill as csk

print("所有人使用一次积点")
game.OnRoundStart()
csk.ParserSkill(1, "jidian", game)
csk.ParserSkill(2, "jidian", game)
csk.ParserSkill(3, "jidian", game)
game.OnRoundEnd()
print(game.GetStatus())

print("#" * 20)
print("1-杀>2, 2-QIN>1, 3非法法攻")
game.OnRoundStart()
ok, msg = csk.ParserSkill(1, "sha 2 1", game)
print(msg)
ok, msg = csk.ParserSkill(2, "qin 1 1", game)
print(msg)
ok, msg = csk.ParserSkill(3, "fagong 1 1", game)
print(msg)
game.OnRoundEnd()
print(game.GetStatus())

print("#" * 20)
