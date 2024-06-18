import asyncio
import pytest

from my_async_package import async_hello


@pytest.mark.asyncio
async def test_async_hello():
    result = await async_hello()
    assert result == "Hello, Async World!"
