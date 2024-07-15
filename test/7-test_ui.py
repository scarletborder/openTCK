# src/test/test_main.py
import sys
import os
import asyncio

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录
project_root = os.path.abspath(os.path.join(current_dir, "../"))

# 将项目根目录添加到 sys.path
sys.path.append(project_root)

from src.utils.pkui.main import Main


if __name__ == "__main__":
    asyncio.run(Main())
