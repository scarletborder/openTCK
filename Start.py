import src.utils.logging.utils as _
import asyncio
import sys
import os

# 将rpc的stub路径添加至环境中
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "./"))
stub_root = os.path.abspath(os.path.join(project_root, "./src/utils/link/stub/"))
sys.path.append(stub_root)

# 自动生成代码
from assets.protos.summon import MakeProtos
from assets.qtui_files.summon import MakeQtUIPyFiles

MakeQtUIPyFiles()
MakeProtos()

from src.ui.adapter.main import Main

if __name__ == "__main__":
    asyncio.run(Main())
