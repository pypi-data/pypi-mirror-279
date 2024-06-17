from __future__ import annotations

import asyncio
import inspect
import os
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Iterable
from typing import Any, ClassVar
from weakref import ReferenceType


class ComponentError(Exception):
    """Raised when a component cannot process correctly"""


class Component(ABC, AsyncIterator):
    """
    A component that can be passed to a pipeline to create a chain of commands.
    Consuming an Iterable and yielding an AsyncIterator.
    It can also be called directly by iterating over its process method with individual values.
    """

    _instances: ClassVar[list[ReferenceType[Component]]] = []
    _type_checking = bool(os.getenv("TYPE_CHECKING", "False"))

    @classmethod
    def instances(cls) -> list[Component]:
        """
        Conveniency class method returning a list of all running instances of Component
        Also remove instances that are not referenced anymore from _instances
        Can be used for graceful shutdown
        """
        return [instance for reference in cls._instances if (instance := reference()) is not None]

    @classmethod
    def register_instance(cls, self: Component) -> None:
        cls._instances.append(ReferenceType(self, cls.remove_instance))

    @classmethod
    def remove_instance(cls, ref: ReferenceType) -> None:
        """
        Remove an instance from the list of tracked instances.
        """
        cls._instances.remove(ref)

    def __init__(self) -> None:
        """
        Init registers the instance. By default an instance does nothing.
        """
        self.__class__.register_instance(self)
        self._prev_component: Component | None = None
        self._source_iter: AsyncIterator
        self._is_running = True

    @property
    def is_running(self) -> bool:
        """
        Can be overriden to define what is_running means.
        """
        return self._is_running

    def stop(self) -> None:
        """
        Can be overriden for custom stop logic.
        """
        self._is_running = False
        if self._prev_component:
            self._prev_component.stop()

    async def _wrap_source(self, source: Source) -> AsyncIterator[Any]:
        """
        A helper method to wrap synchronous iterators with async functionality and yield items.
        """
        if isinstance(source, AsyncIterator):
            async for item in source:
                # Note:
                # For safety we could have a forced await asyncio.sleep(0) here as it is easy to write an async iterator
                # that is never yielding back control to the event loop between iterations but this hurts performance so
                # leaving up to the user to use a valid async iterator that includes at least one await instruction
                yield item
        elif isinstance(source, Iterable):
            for item in source:
                await asyncio.sleep(0)  # Yield control to keep the event loop responsive
                yield item
        else:
            raise ComponentError("Source data must be an Iterable or AsyncIterator.")

    async def _make_source_iter(self, source: Source) -> AsyncIterator[Any]:
        """
        Generate items from the source data and process each item.
        This method combines fetching and processing logic.
        """
        async for item in self._wrap_source(source):
            if self._type_checking:
                self._type_check(item)
            async for processed_item in self.process(item):
                # Same as the note above
                yield processed_item

    def source(self, source: Source) -> Component:
        """
        Transforms a Source into an AsyncIterator and sets it as this component's data source
        """
        if isinstance(source, Component):
            self._prev_component = source
        self._source_iter = self._make_source_iter(source)
        return self

    def __aiter__(self) -> AsyncIterator[Any]:
        return self

    async def __anext__(self) -> Any:
        if not self.is_running:
            raise StopAsyncIteration
        return await self._source_iter.__anext__()

    def _type_check(self, item: Any) -> None:
        """
        If the flag is activated, this function checks the type of items against type hints at runtime
        """
        sig = inspect.signature(self.process)
        for idx, (name, param) in enumerate(sig.parameters.items()):
            if isinstance(item, list | tuple) and not isinstance(item[idx], param.annotation):
                self.stop()
                raise TypeError(
                    f"Parameter '{name}' should be of type {param.annotation}, but was {type(item[idx])} {item[idx]=}"
                )
            if not isinstance(item, param.annotation):
                self.stop()
                raise TypeError(
                    f"Parameter '{name}' should be of type {param.annotation}, but was {type(item)} {item=}"
                )

    @abstractmethod
    async def process(self, item: Any) -> AsyncIterator[Any]:
        """
        Method to be overridden by subclasses to define specific processing logic.
        """
        yield item

    def then(self, component: Component) -> Component:
        """
        Chain another component to process the output of this component.
        """
        component.source(self)
        return component

    async def run(self) -> None:
        """
        Consume all items in this component.
        Can be overriden for custom logic.
        """
        async for _ in self:
            pass


Source = Component | Iterable[Any] | AsyncIterator[Any]
