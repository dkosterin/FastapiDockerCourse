#pip install redis
import asyncio
import redis.asyncio as redis # псевдоним

async def main():
    #decode_responses=True
    client = redis.Redis.from_url("redis://localhost:6379",
                                decode_responses=True
                            )
    await client.set("user", "Ivan")
    user = await client.get("user")
    print(user)
    await client.set("count", "100")
    print(await client.get("count"))
    await client.incrby("count", 20)
    print(await client.get("count"))
    await client.set("temp", "Something", 20)
    await client.aclose()

asyncio.run(main())