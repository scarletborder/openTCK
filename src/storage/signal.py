import asyncio


could_type = asyncio.Event()  # 是否可以输入字符
could_send_action = asyncio.Event()  # 是否可以出招

could_type.set()
could_send_action.clear()
