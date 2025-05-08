import datetime
from dataclasses import dataclass


@dataclass
class PriceHistoryMean:
    market_hash_name: str
    mean: float


@dataclass
class PriceHistoryEntry:

    date: datetime.datetime
    price: float
    volume: float


@dataclass
class PriceHistory:

    market_hash_name: str
    entries: list[PriceHistoryEntry]
