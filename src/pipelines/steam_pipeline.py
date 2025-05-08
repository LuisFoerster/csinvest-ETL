from core.ets import Pipeline
from extractors.steam_extractor import SteamCommunityExtractor
from application.steam.transformer import SteamTransformer
from loader.steam_loader import SteamLoader


def create_steam_pricehistory_pipeline(
    steamcommunity, market_hash_name: str, interval: int = 100, start_delay: int = 0
):

    pipeline = Pipeline()

    pipeline.add_extractor(
        SteamCommunityExtractor(steamcommunity).get_pricehsitory_extractor(
            market_hash_name
        ),
        interval=interval,
        start_delay=start_delay,
        queue_size=1,
    )

    pipeline.add_transformer(
        SteamTransformer().transform_pricehistory,
    )

    pipeline.add_transformer(
        SteamTransformer().calculate_price_history_mean,
    )

    pipeline.add_loader(
        SteamLoader().load_price_history_mean,
    )

    return pipeline
