# src/test/test_main.py
import sys
import os
import asyncio

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录
project_root = os.path.abspath(os.path.join(current_dir, "../"))
stub_root = os.path.abspath(os.path.join(project_root, "./src/utils/link/stub/"))

# 将项目根目录添加到 sys.path
sys.path.append(project_root)
sys.path.append(stub_root)

# 测试,import stub
import src.utils.pkui.main as _
import src.utils.link.stub.gamelink_pb2 as gpb2

aa = gpb2.LobbyPlayer(uid=10, name="he")
print(aa)
