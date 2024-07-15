from prompt_toolkit.application.run_in_terminal import run_in_terminal
from src.utils.pkui.widgets import (
    Input_Area,
    Output_Chat_Area,
    Output_Status_Area,
    Output_Tip_Area,
    Bindings,
)


class NewUI:
    """UI暴露方法"""

    @staticmethod
    def PrintChatArea(s, end="\n"):
        buffer = Output_Chat_Area.buffer
        # window = output_chat_area.window

        # 检查 TextArea 是否在最低端
        is_at_bottom = buffer.document.cursor_position == len(buffer.text)

        # 在终端中运行以确保线程安全
        buffer.text += s + end

        # 如果在最低端，则滚动到底部
        if is_at_bottom:
            run_in_terminal(lambda: buffer.cursor_down(len(buffer.text)))

    @staticmethod
    def PrintStatusArea(s):
        Output_Status_Area.text = s

    @staticmethod
    def PrintTipArea(s):
        Output_Tip_Area.text = s
