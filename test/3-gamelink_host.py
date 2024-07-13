"""
test03
测试联机，不涉及交互界面

此文件将作为服务端


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

from src.utils.link.player_link import HostPlayerLink


"""
运行时
一个Link 实例
一个Lobby 实例

一个Game 实例


"""


async def Main():
    my_host = HostPlayerLink()
    await my_host.JoinLobby()


import asyncio

if __name__ == "__main__":
    asyncio.run(Main())
