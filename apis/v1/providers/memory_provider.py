from typing import Any
import os


class MemoryProvider:
    """
    MemoryProvider is a class that provides data from memory.
    """

    def __init__(self, cache_dir: str = "cache"):
        self.cache = {}
        self.cache_dir = os.path.join(os.getcwd(), cache_dir)

        # Initialize cache directory
        os.makedirs(self.cache_dir, exist_ok=True)

    def get(self, key: str) -> Any | None:
        # Get value from cache
        return self.cache.get(key, None)

    def gets(self, keys: list[str]) -> list[Any] | None:
        # Get values from cache
        caches = [self.cache.get(key, None) for key in keys]
        if len(caches) == 0:
            return None
        return caches

    def set(self, key: str, value: Any) -> None:
        # Set value in cache
        self.cache[key] = value

    def sets(self, data: dict, ttl: int = None) -> None:
        # Set values in cache
        for key, value in data.items():
            self.cache[key] = value

    def remove(self, key: str) -> None:
        # Remove value from cache
        self.cache.pop(key, None)

    def removes(self, keys: list[str]) -> None:
        # Remove values from cache
        for key in keys:
            self.cache.pop(key, None)
        if not self.in_memory:
            self.__save()

    def save_cache_file(self, data: bytes, filename: str) -> str:
        # Save file to cache
        cache_file_path = os.path.join(self.cache_dir, filename)
        with open(cache_file_path, "wb") as f:
            f.write(data)
        return cache_file_path

    def remove_cache_file(self, filename: str) -> None:
        # Remove file from cache
        cache_file_path = os.path.join(self.cache_dir, filename)
        os.remove(cache_file_path)

    def reset_cache(self) -> None:
        # Reset cache
        self.cache = {}
