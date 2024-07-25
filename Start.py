import src.utils.logging.utils as _
import asyncio
import sys
import os

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录
project_root = os.path.abspath(os.path.join(current_dir, "./"))
stub_root = os.path.abspath(os.path.join(project_root, "./src/utils/link/stub/"))

# 将项目根目录添加到 sys.path
# sys.path.append(project_root)
sys.path.append(stub_root)

from src.ui.adapter.main import Main


if __name__ == "__main__":
    asyncio.run(Main())
