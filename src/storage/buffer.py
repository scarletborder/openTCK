import asyncio

Input_Content = ""
InpLock = asyncio.Event()


async def ReadInput() -> str:
    global Input_Content
    await InpLock.wait()
    InpLock.clear()
    tmp = Input_Content
    Input_Content = ""
    return tmp


async def SetInput(s) -> None:
    global Input_Content
    Input_Content = s
    InpLock.set()
