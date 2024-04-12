from typing import Any, AnyStr, ByteString
import os
import json
from threading import Timer
from ..utils.logger import log_cache


class CacheProvider:
    def __init__(
        self,
        cache_file_name: AnyStr = "__cache__.json",
        cache_dir: AnyStr = "cache",
        in_memory: bool = False
    ):
        self.cache_dir = os.path.join(os.getcwd(), cache_dir)
        self.cache_path = os.path.join(
            os.getcwd(), cache_dir, cache_file_name)
        self.cache = self.__load()
        self.in_memory = in_memory

    def __load(self):
        # Load cache from file
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r") as _file:
                return json.load(_file)
        # Create cache file if it does not exist
        else:
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            with open(self.cache_path, "w") as _file:
                _file.write("{}")
            return {}

    def __save(self):
        # Save cache to file
        with open(self.cache_path, "w") as _file:
            json.dump(self.cache, _file)
            _file.close()

    def get(self, key: str) -> Any | None:
        # Get value from cache
        data = self.cache.get(key, None)
        if not data:
            log_cache(f"Cache miss for {key}")
        else:
            log_cache(f"Cache hit for {key}")
        return data

    def gets(self, keys: list[str]) -> list[Any] | None:
        # Get values from cache
        caches = [self.cache.get(key, None) for key in keys]
        if len(caches) == 0:
            return None
        return caches

    def set(self, key: AnyStr, value: Any, ttl: int = None) -> None:
        # Set value in cache
        self.cache[key] = value
        log_cache(f"Set cache for {key}")
        # Set timer to remove value from cache
        if ttl:
            Timer(ttl, self.remove, [key]).start()
        # Only save when in_memory is False
        if not self.in_memory:
            self.__save()

    def sets(self, data: dict, ttl: int = None) -> None:
        # Set values in cache
        for key, value in data.items():
            self.cache[key] = value
        # Set timer to remove value from cache
        if ttl:
            Timer(ttl, self.removes, [[key for key in data.keys()]]).start()
        # Only save when in_memory is False
        if not self.in_memory:
            self.__save()

    def remove(self, key: str) -> None:
        # Remove value from cache
        self.cache.pop(key, None)
        log_cache(f"Remove cache for {key}")
        if not self.in_memory:
            self.__save()

    def removes(self, keys: list[str]) -> None:
        # Remove values from cache
        for key in keys:
            self.cache.pop(key, None)
        if not self.in_memory:
            self.__save()

    def save_cache_file(self, data: ByteString, filename: AnyStr) -> AnyStr:
        # Save file to cache
        cache_file_path = os.path.join(self.cache_dir, filename)
        with open(cache_file_path, "wb") as f:
            f.write(data)
        log_cache(f"Save cache file for {filename}")
        return cache_file_path

    def remove_cache_file(self, filename: AnyStr) -> None:
        # Remove file from cache
        cache_file_path = os.path.join(self.cache_dir, filename)
        os.remove(cache_file_path)
        log_cache(f"Remove cache file for {filename}")

    def reset_cache(self) -> None:
        # Reset cache
        self.cache = {}
        log_cache("Cache burst!")
        if not self.in_memory:
            self.__save()
