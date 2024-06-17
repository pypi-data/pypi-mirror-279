from collections.abc import AsyncIterator

import pytest

from aiterio import Component, ComponentError


class AddOne(Component):
    async def process(self, item: int) -> AsyncIterator[int]:
        yield item + 1


class Multiply(Component):
    def __init__(self, factor: int = 1) -> None:
        super().__init__()
        self._factor = factor

    async def process(self, item: int) -> AsyncIterator[int]:
        yield item * self._factor


async def test_processing_integers() -> None:
    component = AddOne().source(range(5))
    result = [value async for value in component]
    assert result == [1, 2, 3, 4, 5]


async def test_multiple_components() -> None:
    pipeline = AddOne().source(range(5)).then(Multiply(factor=2))
    result = [value async for value in pipeline]
    assert result == [2, 4, 6, 8, 10]


async def test_non_iterator_source() -> None:
    component = AddOne().source(1234)  # type: ignore[arg-type]
    with pytest.raises(ComponentError):
        await component.run()


async def test_type() -> None:
    Component._type_checking = True  # noqa: SLF001
    component = AddOne().source(["a", "b", "c"])
    with pytest.raises(TypeError):
        await component.run()
    Component._type_checking = False  # noqa: SLF001
