import asyncio


def RunAsync(func):
    def wrapper(*args, **kwargs):
        asyncio.create_task(func(*args, **kwargs))

    return wrapper
