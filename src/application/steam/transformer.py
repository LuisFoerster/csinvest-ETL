from domain.models import PriceHistory, PriceHistoryEntry, PriceHistoryMean
from application.steam.dto import SteamPriceHistoryDTO
import datetime


def parse_date(date_str: str) -> datetime.datetime:
    """
    Parse a date string from the Steam API.
    date_str is like "May 07 2025 15: +4" (%b %d %Y %H: %z) but not correctly formatted for datetime.datetime.strptime
    """
    # date_base is like "May 07 2025 15:"
    # timezone_base is like "4" or "15"
    datetime_base, timezone_base = date_str.rsplit("+", 1)

    # if 4 -> 04, but 15 -> 15 and add :00 -> +04:00, +15:00
    timezone_corrected = f"+{timezone_base.zfill(2)}:00"

    # if "May 07 2025 15:" -> "May 07 2025 +15:00"
    datetime_corrected = datetime_base.rsplit(":", 1)[0]

    # if "May 07 2025 15: +04" -> "May 07 2025 15 +04:00"
    datetime_str = f"{datetime_corrected} {timezone_corrected}"

    return datetime.datetime.strptime(datetime_str, "%b %d %Y %H %z")


class SteamTransformer:

    async def transform_pricehistory(
        self, steam_pricehistory: SteamPriceHistoryDTO
    ) -> PriceHistory:
        return PriceHistory(
            market_hash_name=steam_pricehistory.market_hash_name,
            entries=[
                PriceHistoryEntry(
                    date=parse_date(entry[0]), price=entry[1], volume=entry[2]
                )
                for entry in steam_pricehistory.prices
            ],
        )

    async def calculate_price_history_mean(
        self, price_history: PriceHistory
    ) -> PriceHistoryMean:

        mean = sum(
            [price_history_entry.price for price_history_entry in price_history.entries]
        ) / len(price_history.entries)
        return PriceHistoryMean(
            market_hash_name=price_history.market_hash_name, mean=mean
        )
