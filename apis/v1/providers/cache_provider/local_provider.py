from typing import AnyStr
from typing_extensions import override
import os
import orjson
from threading import Timer
from .base_provider import BaseCacheProvider


class LocalCacheProvider(BaseCacheProvider):
    def __init__(
        self,
        expiration: int = 360,
        cache_file_name: AnyStr = "__cache__.json",
        cache_dir: AnyStr = "data"
    ):
        super().__init__(expiration)
        self.cache_dir = os.path.join(os.getcwd(), cache_dir)
        self.cache_path = os.path.join(
            os.getcwd(), cache_dir, cache_file_name)
        self.cache = self.__load()

    def __load(self) -> dict:
        # Load cache from file
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "rb") as _file:
                return orjson.loads(_file.read())
        # Create cache file if it does not exist
        else:
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            with open(self.cache_path, "w") as _file:
                _file.write("{}")
            return {}

    def __save(self):
        # Save cache to file
        with open(self.cache_path, "wb") as _file:
            _file.write(orjson.dumps(self.cache))
            _file.close()

    @override
    def get(self, key):
        # Get value from cache
        return self.cache.get(key, None)

    @override
    def gets(self, keys):
        # Get values from cache
        return [self.cache.get(key, None) for key in keys]

    @override
    def set(self, key, value, ttl=None, merge=False):
        # Set value in cache
        if merge and key in self.cache:
            self.cache[key].update(value)
        else:
            self.cache[key] = value
        # Set timer to remove value from cache
        if ttl or self.expiration:
            Timer(ttl or self.expiration, self.delete, [key]).start()
        self.__save()

    @override
    def sets(self, data, ttl=None):
        # Set values in cache
        for key, value in data.items():
            self.cache[key] = value
        # Set timer to remove value from cache
        if ttl or self.expiration:
            Timer(ttl or self.expiration, self.deletes, [
                  [key for key in data.keys()]]).start()
        self.__save()

    @override
    def delete(self, key):
        # Remove value from cache
        self.cache.pop(key, None)
        self.__save()

    @override
    def deletes(self, keys):
        # Remove values from cache
        for key in keys:
            self.cache.pop(key, None)
        self.__save()

    @override
    def clear(self):
        self.cache = {}
        self.__save()
