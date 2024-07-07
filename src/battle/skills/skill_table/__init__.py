import os
import glob
import importlib

# 获取当前文件夹路径
package_dir = os.path.dirname(__file__)

# 找到所有的 .py 文件，但排除 __init__.py 本身
modules = glob.glob(os.path.join(package_dir, "*.py"))
modules = [
    os.path.basename(f)[:-3]
    for f in modules
    if os.path.isfile(f) and not f.endswith("__init__.py")
]

# 动态导入所有的模块
for module in modules:
    importlib.import_module(f".{module}", package=__name__)
