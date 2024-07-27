import os
import glob
import shutil


def MakeProtos():
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 获取src目录
    src_root = os.path.abspath(os.path.join(current_dir, "../../src/"))
    protos_dir = os.path.abspath(os.path.join(current_dir, "./"))
    stub_dir = os.path.abspath(os.path.join(src_root, "./utils/link/stub/"))

    # ensure specified directory
    if os.path.exists(stub_dir) is True:
        shutil.rmtree(stub_dir, True)

    os.makedirs(stub_dir)

    proto_files = glob.glob(f"{protos_dir}/*.proto")
    for proto_file in proto_files:
        os.system(
            f"python -m grpc_tools.protoc -I{protos_dir} --python_out={stub_dir} --pyi_out={stub_dir} --grpc_python_out={stub_dir} {proto_file}"
        )


if __name__ == "__main__":
    MakeProtos()
