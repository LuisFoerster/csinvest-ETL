from core.ets.extractor import Extractor
from core.ets.transformer import Transformer
from core.ets.loader import Loader
from typing import Callable, Any, Coroutine
import logging

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, name: str = "unnamed"):
        self.name = name
        self.extractor: Extractor = None
        self.transformers: list[Transformer] = []
        self.loader: Loader = None

    def add_extractor(
        self,
        extract_function: Callable[[], Coroutine[None, None, Any]],
        start_delay: int = 0,
        interval: int = 3,
        queue_size: int | None = None,
        on_error: Callable[[Exception], Coroutine[None, None, None]] = None,
    ):
        self.extractor = Extractor(
            extract_function=extract_function,
            start_delay=start_delay,
            interval=interval,
            queue_size=queue_size,
            on_error=on_error,
        )

    def add_transformer(
        self, transform_function: Callable[[Any], Coroutine[None, None, Any]]
    ):
        if self.extractor is None and not self.transformers:
            raise ValueError(
                "Pipeline must start with an extractor before transformers."
            )

        source = self.transformers[-1] if self.transformers else self.extractor
        self.transformers.append(
            Transformer(
                source=source,
                transform_function=transform_function,
            )
        )

    def add_loader(self, load_function: Callable[[Any], Coroutine[None, None, None]]):
        if len(self.transformers) == 0:
            raise ValueError(
                "Pipeline must start with an extractor before transformers."
            )
        if self.loader is not None:
            raise ValueError("Loader has already been set")
        self.loader = Loader(
            source=self.transformers[-1],
            load_function=load_function,
        )

    async def run(self):
        if not self.loader:
            raise RuntimeError("No loader set. Cannot run pipeline.")
        try:
            async for _ in self.loader:
                pass
        except Exception as e:
            logger.exception(f"Pipeline execution failed: {e}")
            raise

    def stop(self):
        try:
            self.extractor.stop()
        except Exception as e:
            logger.exception(f"Error stopping extractor: {e}")
