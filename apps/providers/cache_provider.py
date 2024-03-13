import os
import json
from threading import Timer


class CacheProvider:
    def __init__(
        self,
        cache_file_name: str = "__cache__.json",
        cache_dir: str = "cache"
    ):
        self.cache_dir = os.path.join(os.getcwd(), cache_dir)
        self.cache_path = os.path.join(
            os.getcwd(), cache_dir, cache_file_name)
        self.cache = self.__load()

    def __load(self):
        # Load cache from file
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r") as file:
                return json.load(file)
        # Create cache file if it does not exist
        else:
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            with open(self.cache_path, "w") as file:
                file.write("{}")
            return {}

    def __save(self):
        # Save cache to file
        with open(self.cache_path, "w") as file:
            json.dump(self.cache, file)

    def get(self, key: str):
        # Get value from cache
        return self.cache.get(key, None)

    def set(self, key: str, value, ttl: int = None):
        # Set value in cache
        self.cache[key] = value
        # Set timer to remove value from cache
        if ttl:
            Timer(ttl, self.remove, [key]).start()
        self.__save()

    def remove(self, key: str):
        # Remove value from cache
        self.cache.pop(key, None)
        self.__save()

    def save_cache_file(self, file: bytes, filename: str):
        # Save file to cache
        cache_file_path = os.path.join(self.cache_dir, filename)
        with open(cache_file_path, "wb") as f:
            f.write(file)
        return cache_file_path

    def remove_cache_file(self, filename: str):
        # Remove file from cache
        cache_file_path = os.path.join(self.cache_dir, filename)
        os.remove(cache_file_path)
