import orjson
from typing_extensions import override
from ...configs.redis_config import cache_db
from .base_provider import BaseCacheProvider


class RedisCacheProvider(BaseCacheProvider):
    def __init__(self, expiration: int = 360):
        super().__init__(expiration)

    @override
    def get(self, key):
        str_value = cache_db.get(key)
        if str_value is None:
            return None
        return orjson.loads(str_value)

    @override
    def gets(self, keys):
        str_values = cache_db.mget(keys)
        return [orjson.loads(value) if value else None for value in str_values]

    @override
    def set(self, key, value, ttl=None, merge=None):
        str_value = orjson.dumps(value).decode("utf-8")
        cache_db.set(key, str_value, ex=ttl or self.expiration)

    @override
    def sets(self, data: dict, ttl: int = None):
        pipe = cache_db.pipeline()
        for key, value in data.items():
            str_value = orjson.dumps(value).decode("utf-8")
            pipe.set(key, str_value, ex=ttl or self.expiration)
        pipe.execute()

    @override
    def delete(self, key):
        cache_db.delete(key)

    @override
    def deletes(self, keys):
        cache_db.delete(*keys)

    @override
    def clear(self):
        cache_db.flushdb()
