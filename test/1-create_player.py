"""
test01
测试能否正常的创建多个角色加入战局，并显示信息
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
