import asyncio
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window
from prompt_toolkit.widgets import TextArea, MenuContainer, MenuItem, Button
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.styles import Style

input_area = TextArea(height=1, prompt="Input: ", multiline=False)

# 主要左边的对话框，和命令的输出框
output_chat_area = TextArea(style="class:output-area", focusable=False, scrollbar=True)
# 主要右上的状态信息
output_status_area = TextArea(
    style="class:output-area",
    focusable=False,
    scrollbar=False,
    wrap_lines=False,
    text="halo1",
)
output_tip_area = TextArea(
    style="class:output-area", focusable=False, scrollbar=False, height=1, text="halo2"
)

bindings = KeyBindings()


@bindings.add("c-c")
@bindings.add("c-q")
def _(event):
    event.app.exit()


def Main():
    # 创建菜单
    menu = MenuContainer(
        body=HSplit(
            [
                VSplit(
                    [output_chat_area, HSplit([output_status_area, output_tip_area])]
                ),
                input_area,
            ]
        ),
        menu_items=[
            MenuItem(
                "File",
                children=[
                    MenuItem(
                        "Open",
                        handler=lambda: output_chat_area.buffer.insert_text(
                            "Open selected\n"
                        ),
                    ),
                    MenuItem(
                        "Save",
                        handler=lambda: output_chat_area.buffer.insert_text(
                            "Save selected\n"
                        ),
                    ),
                    MenuItem("Exit", handler=lambda: app.exit()),
                ],
            ),
            MenuItem(
                "Edit",
                children=[
                    MenuItem(
                        "Cut",
                        handler=lambda: output_chat_area.buffer.insert_text(
                            "Cut selected\n"
                        ),
                    ),
                    MenuItem(
                        "Copy",
                        handler=lambda: output_chat_area.buffer.insert_text(
                            "Copy selected\n"
                        ),
                    ),
                    MenuItem(
                        "Paste",
                        handler=lambda: output_chat_area.buffer.insert_text(
                            "Paste selected\n"
                        ),
                    ),
                ],
            ),
            MenuItem(
                "Help",
                children=[
                    MenuItem(
                        "About",
                        handler=lambda: output_chat_area.buffer.insert_text(
                            "About selected\n"
                        ),
                    ),
                ],
            ),
        ],
    )

    # 创建应用程序
    app = Application(
        layout=Layout(menu),
        key_bindings=bindings,
        full_screen=True,
        color_depth=ColorDepth.TRUE_COLOR,
    )

    app.run()


if __name__ == "__main__":
    Main()
