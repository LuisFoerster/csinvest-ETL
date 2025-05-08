from connector.steam import SteamCommunityConnector
from application.steam.dto import SteamPriceHistoryDTO
from typing import Callable, Coroutine


class SteamCommunityExtractor:

    def __init__(self, steamcommunity_connector: SteamCommunityConnector):
        self.steamcommunity_connector = steamcommunity_connector

    def get_pricehsitory_extractor(
        self, market_hash_name: str
    ) -> Callable[[], Coroutine[None, None, SteamPriceHistoryDTO]]:
        async def pricehistory_extractor():
            response = await self.steamcommunity_connector.get_pricehistory(
                market_hash_name
            )
            return SteamPriceHistoryDTO(
                market_hash_name=market_hash_name, prices=response["prices"]
            )

        return pricehistory_extractor
