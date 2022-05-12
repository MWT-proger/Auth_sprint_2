from abc import ABC, abstractmethod


class CacheBase(ABC):
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value: str, expire: int) -> None:
        pass


class ElasticBase(ABC):

    @abstractmethod
    def get_by_id(self, index: str, dataclass, key: str):
        pass

    @abstractmethod
    def search_data(self, query=None, index=None, dataclass=None, size=None, number=None):
        pass
