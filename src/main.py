from pipelines.steam_pipeline import create_steam_pricehistory_pipeline
import asyncio
from connector.steam import SteamConnector
from core.settings import settings

MARKET_HASH_NAMES = [
    "Chroma Case",
    "Chroma 2 Case",
    "Chroma 3 Case",
    "Spectrum Case",
    "Spectrum 2 Case",
    "Gamma Case",
    "Gamma 2 Case",
    "CS:GO Weapon Case",
    "CS:GO Weapon Case 2",
    "CS:GO Weapon Case 3",
    "Fracture Case",
    "Prisma Case",
    "Prisma 2 Case",
]

UPDATE_INTERVAL = 30  # Seconds


async def main():

    steam = SteamConnector(
        username=settings.STEAM_USERNAME,
        password=settings.STEAM_PASSWORD,
        api_key=settings.STEAM_WEB_API_KEY,
    )

    # Delay between each pipeline start
    delay_factor = UPDATE_INTERVAL / len(MARKET_HASH_NAMES)

    tasks = []
    for i, market_hash_name in enumerate(MARKET_HASH_NAMES):
        pipeline = create_steam_pricehistory_pipeline(
            steam.community,
            market_hash_name,
            interval=UPDATE_INTERVAL,
            start_delay=delay_factor * i,
        )
        task = asyncio.create_task(pipeline.run())
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
