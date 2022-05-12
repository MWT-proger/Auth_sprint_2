from abc import ABC, abstractmethod
from typing import Optional

from db.interfaces import CacheBase, ElasticBase
from tools.cacheable import cacheable


class BaseView(ABC):
    def __init__(self, cache: CacheBase, elasticsearch: ElasticBase):
        self.cache = cache
        self.elasticsearch = elasticsearch
        self.key = None

    @property
    @abstractmethod
    def index(self):
        pass

    @property
    @abstractmethod
    def model(self):
        pass


class ListView(BaseView, ABC):
    @abstractmethod
    def _get_key(self, **kwargs) -> Optional[str]:
        pass

    @abstractmethod
    def _get_search_request(self, **kwargs) -> Optional[dict]:
        pass

    @cacheable()
    async def get_specific_data(self,
                                query_search: str = None,
                                sort: str = None,
                                filter_genre: str = None,
                                page_size: int = 50,
                                page_number: int = 1,
                                ):
        self.key = self._get_key(query_search=query_search,
                                 sort=sort,
                                 filter_genre=filter_genre,
                                 page_size=page_size,
                                 page_number=page_number)
        items = await self.cache.get(self.index, key=self.key)
        if not items:
            body = self._get_search_request(
                query_search=query_search,
                sort=sort,
                filter_genre=filter_genre
            )
            items = await self.elasticsearch.search_data(
                query=body,
                index=self.index,
                size=page_size,
                number=page_number
            )
            if not items:
                return None
        return [self.model.parse_obj(item) for item in items]


class DetailView(BaseView, ABC):
    @cacheable()
    async def get_by_id(self, id: str):
        item = await self.cache.get(self.index, key=id)

        if not item:
            item = await self.elasticsearch.get_by_id(self.index, key=id)
            if not item:
                return None
        return self.model.parse_obj(item)
