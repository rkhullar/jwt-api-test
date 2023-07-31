from collections.abc import AsyncIterable
from typing import TypeVar

T = TypeVar('T')


async def async_list(stream: AsyncIterable[T]) -> list[T]:
    return [item async for item in stream]
