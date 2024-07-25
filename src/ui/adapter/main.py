from src.constant.config.ui_type import UITYPE


async def Main(): ...


if UITYPE == "pkui":
    from src.ui.pkui.main import Main as m

    Main = m
elif UITYPE == "qtui":
    from src.ui.qtui.main import Main as m

    Main = m
else:
    print("No that UI type you required")
    exit(1)
