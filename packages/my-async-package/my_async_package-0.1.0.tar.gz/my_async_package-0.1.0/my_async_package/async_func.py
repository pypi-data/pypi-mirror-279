import asyncio


async def async_hello():
    await asyncio.sleep(1)
    return "Hello, Async World!"
