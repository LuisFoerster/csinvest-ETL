from domain.models import PriceHistoryMean
import asyncio
import random


class SteamLoader:

    async def load_price_history_mean(self, price_history_mean: PriceHistoryMean):
        """
        Imagine this is a database connection and we save the price history mean to the database.
        """
        await asyncio.sleep(random.randint(1, 5))
        print(price_history_mean)
