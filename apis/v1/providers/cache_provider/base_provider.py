from typing import Any
from abc import abstractmethod


class BaseCacheProvider:
    def __init__(self, expiration: int):
        self.expiration = expiration

    @abstractmethod
    def get(self, key: str) -> Any | None:
        """
        Get value from cache.
        """
        raise NotImplementedError

    @abstractmethod
    def gets(self, keys: list[str]) -> list[Any | None]:
        """
        Get values from cache.
        """
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: dict, ttl: int = None, merge: bool = None) -> None:
        """
        Set value in cache.
        Merge only available when value is a dict.
        """
        raise NotImplementedError

    @abstractmethod
    def sets(self, data: dict, ttl: int = None) -> None:
        """
        Set values in cache.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Delete value from cache.
        """
        raise NotImplementedError

    @abstractmethod
    def deletes(self, keys: list[str]) -> None:
        """
        Delete values from cache.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """
        Brust cache.
        """
        raise NotImplementedError
