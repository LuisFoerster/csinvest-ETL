from typing import AsyncGenerator, Callable, Coroutine, TypeVar

T = TypeVar("T")


class Loader:
    """
    Loads data from a source and loads it into a target.
    """

    def __init__(
        self,
        source: AsyncGenerator[T, None],
        load_function: Callable[[T], Coroutine[None, None, None]],
    ):
        """
        Args:
            source: The source to get the data from.
            load_function: The function to load the data into the target.
        """
        self.source = source
        self.load_function = load_function

    async def __aiter__(self) -> AsyncGenerator[T, None]:
        async for data in self.source:
            await self.load_function(data)
            yield
