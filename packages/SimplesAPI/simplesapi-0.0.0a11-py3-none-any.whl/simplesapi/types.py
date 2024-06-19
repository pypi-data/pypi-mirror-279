from abc import ABC


class Database(ABC):
    def __init__(self): ...


class Cache:
    def __init__(self, redis):
        self.redis = redis

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: str, ex: int):
        await self.redis.set(key, value, expire=ex)

    async def ping(self):
        return await self.redis.ping()

    async def lock(self, key: str, timeout: int = 30):
        lock_key = f"{key}:lock"
        lock = await self.redis.setnx(lock_key, "locked")
        if timeout:
            await self.redis.expire(lock_key, timeout)
        return lock

    async def unlock(self, key: str):
        lock_key = f"{key}:lock"
        await self.redis.delete(lock_key)

    async def close(self):
        await self.redis.close()
