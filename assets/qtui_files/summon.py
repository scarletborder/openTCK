import os
import glob
import shutil


def MakeQtUIPyFiles():
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 获取src目录
    src_root = os.path.abspath(os.path.join(current_dir, "../../src/"))
    ui_dir = os.path.abspath(os.path.join(current_dir, "./"))
    stub_dir = os.path.abspath(os.path.join(src_root, "./ui/qtui/widgets/"))

    # ensure specified directory
    if os.path.exists(stub_dir) is True:
        shutil.rmtree(stub_dir, True)

    os.makedirs(stub_dir)

    ui_files = glob.glob(f"{ui_dir}/*.ui")
    for ui_file in ui_files:
        new_py_name = ui_file.split(os.path.sep)[-1].strip(".ui") + ".py"
        os.system(f"pyuic6 -x {ui_file} -o {stub_dir}/{new_py_name}")


if __name__ == "__main__":
    MakeQtUIPyFiles()
