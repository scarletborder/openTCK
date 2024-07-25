import asyncio


class TaskPool:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def add_task(self, message):
        await self.queue.put(message)

    async def get_task(self):
        task = await self.queue.get()
        return task

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        while not self.queue.empty():
            await asyncio.sleep(0.1)
