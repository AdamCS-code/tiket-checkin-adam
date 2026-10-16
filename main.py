import asyncio

redis_table = {"exchange_rate": {"sgd": 1.0, "idr": 10000.0}}
cache = {}


async def get_from_redis():
    # Simulate getting data from Redis
    await asyncio.sleep(1)  # Simulate network delay
    return redis_table["exchange_rate"].copy()


async def update_from_redis(ttl=5):
    while True:
        await asyncio.sleep(ttl)
        redis_table["exchange_rate"]["idr"] += 100.0
        cache.pop("exchange_rate", None)
        print(f"Redis updated after {ttl}s: {redis_table['exchange_rate']}")


async def update_database():
    # simulate request updating that updates the database and redis
    await asyncio.sleep(2)  # Simulate network delay
    # we have to throw all the cache away because the data in redis is updated
    redis_table["exchange_rate"]["idr"] += 500.0
    cache.pop("exchange_rate", None)
    print(f"Database updated: {redis_table['exchange_rate']}")

async def main():
    update_task = asyncio.create_task(update_from_redis())
    try:
        for _ in range(30):

            if _ == 10:
                await update_database()
            
            if "exchange_rate" in cache:
                print("Cache hit")
                data = cache["exchange_rate"]
            else:
                print("Cache miss")
                data = await get_from_redis()
                cache["exchange_rate"] = data

            print(data)
            await asyncio.sleep(1)
    finally:
        update_task.cancel()
        try:
            await update_task
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    asyncio.run(main())
