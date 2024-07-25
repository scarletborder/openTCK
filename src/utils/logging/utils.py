from src.utils.pkui.utils import NewUI
import grpc
import sys
import logging


def Errorln(msg: str):
    NewUI.PrintChatArea("[ERROR]" + msg)


def Warnln(msg: str):
    NewUI.PrintChatArea("[WARN]" + msg)


def Infoln(msg: str):
    NewUI.PrintChatArea("[INFO]" + msg)


class MyCustomOutput:
    def write(self, message):
        # 在这里可以定义任何你希望的输出处理逻辑
        # 比如写入文件、发送到网络等
        Infoln(message)

    def flush(self):
        pass  # 通常情况下需要定义flush方法，但在这里我们不需要做任何事情


class CustomLogHandler(logging.Handler):
    def __init__(self, custom_output):
        super().__init__()
        self.custom_output = custom_output

    def emit(self, record):
        log_entry = self.format(record)
        self.custom_output.write(log_entry + "\n")


# 创建 MyCustomOutput 的实例
custom_output = MyCustomOutput()

# 创建自定义日志处理器，并传入 MyCustomOutput 实例
custom_handler = CustomLogHandler(custom_output)
custom_handler.setLevel(logging.DEBUG)

# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
custom_handler.setFormatter(formatter)

# 获取根日志记录器并添加自定义处理器
root_logger = logging.getLogger()
root_logger.addHandler(custom_handler)
root_logger.setLevel(logging.DEBUG)

# 配置 gRPC 的日志
grpc_logger = logging.getLogger("grpc")
grpc_logger.setLevel(logging.DEBUG)
grpc_logger.addHandler(custom_handler)

# 禁用 gRPC 内部日志处理器，以避免重复输出
grpc_logger.propagate = False

# 将自定义处理器添加到 gRPC 的日志记录器中
grpc_logger.addHandler(custom_handler)


class StderrRedirector:
    def __init__(self, custom_output):
        self.custom_output = custom_output

    def write(self, message):
        if message.strip():  # 过滤掉空行
            self.custom_output.write(message)

    def flush(self):
        pass  # 通常情况下需要定义flush方法，但在这里我们不需要做任何事情


# 重定向 stderr 到 MyCustomOutput
sys.stderr = StderrRedirector(custom_output)
