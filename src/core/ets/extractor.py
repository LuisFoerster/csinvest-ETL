from typing import Callable, Coroutine, AsyncGenerator, TypeVar
import logging
import functools
import time
import asyncio


logger = logging.getLogger(__name__)

T = TypeVar("T")


class Extractor:
    """
    A class that extracts data from a source at regular intervals.
    The extract function is repeatedly called while the extractor is running.
    """

    def __init__(
        self,
        extract_function: Callable[[], Coroutine[None, None, T]],
        interval: int = 3,
        start_delay: int = 0,
        queue_size: int | None = 1,
        on_error: Callable[[Exception], Coroutine[None, None, None]] = None,
    ):
        """
        Args:
            request_function: A function that returns a response.
            interval: The interval in seconds between requests.
            start_delay: The delay in seconds before the first extraction.
            queue_size: The size of the queue to store the results.
            on_error: A function that is called when an error occurs.
        """
        self.extract_function = extract_function

        self.interval = interval
        self.on_error = on_error
        self.start_delay = start_delay

        if queue_size is not None:
            self.queue = asyncio.Queue(queue_size)
        else:
            self.queue = asyncio.Queue()

        self._running = False
        self._task = None

    def _get_function_name(self, function: Callable[[], Coroutine[None, None, T]]):
        if isinstance(function, functools.partial):
            return function.func.__name__

        else:
            return function.__name__

    async def _run(self):
        await asyncio.sleep(self.start_delay)
        while self._running:
            start = time.monotonic()

            try:
                result = await self.extract_function()
                await self.queue.put(result)
            except Exception as e:
                if self.on_error:
                    await self.on_error(e)
                func_name = self._get_function_name(self.extract_function)
                logger.error(f"Error in {func_name}: {e}")

            # Time taken to execute the extraction and queue the result
            time_delta = time.monotonic() - start

            time_to_wait = self.interval - time_delta

            if time_to_wait > 0:
                # Wait for the remaining time to maintain the interval
                await asyncio.sleep(time_to_wait)
            elif time_to_wait < 0:
                # If extractions was skipped because subsequent processing was too slow, don't wait for the next interval.
                # Get the next extraction directly.
                missed_extractions = round(time_delta / self.interval, 0)
                func_name = self._get_function_name(self.extract_function)
                logger.warning(
                    f"Extractor {func_name} missed {missed_extractions} extractions"
                )

    async def __aiter__(self) -> AsyncGenerator[T, None]:
        self.start()
        while self._running:
            yield await self.queue.get()

    def start(self):
        if not self._task:
            self._task = asyncio.create_task(self._run())
        self._running = True

    def stop(self):
        if self._task:
            self._task.cancel()
        self._running = False
