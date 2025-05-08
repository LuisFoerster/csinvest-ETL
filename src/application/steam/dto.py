from pydantic import BaseModel


class SteamPriceHistoryDTO(BaseModel):

    market_hash_name: str
    prices: list[tuple[str, float, int]]
