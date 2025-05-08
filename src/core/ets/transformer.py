from typing import (
    Callable,
    TypeVar,
    AsyncGenerator,
    Coroutine,
)
import logging
import functools


logger = logging.getLogger(__name__)


T_in = TypeVar("T_in")
T_out = TypeVar("T_out")


class Transformer:

    def __init__(
        self,
        source: AsyncGenerator[T_in, None],
        transform_function: Callable[[T_in], Coroutine[None, None, T_out]],
    ):
        """
        Args:
            source: The source to get the data from.
            transform_function: The function to transform the data. FIRST ARGUMENT MUST BE THE DATA to transform.
        """
        self.source = source
        self.transform_function = transform_function

    async def __aiter__(self) -> AsyncGenerator[T_out, None]:
        async for data in self.source:

            try:
                transformed = await self.transform_function(data)
                yield transformed
            except Exception as e:
                if isinstance(self.transform_function, functools.partial):
                    func_name = self.transform_function.func.__name__
                else:
                    func_name = self.transform_function.__name__
                logger.error(f"Error in {func_name}: {e}")
