from typing import Optional

import backoff
from db.interfaces import ElasticBase
from elasticsearch import AsyncElasticsearch, ConnectionError, NotFoundError

es: Optional[AsyncElasticsearch] = None


async def get_elastic() -> AsyncElasticsearch:
    return es


class ElasticService(ElasticBase):
    def __init__(self, elasticsearch: AsyncElasticsearch):
        self.elasticsearch = elasticsearch

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def get_by_id(self, index: str, key: str):
        try:
            doc = await self.elasticsearch.get(index, key)
        except NotFoundError:
            return None
        return doc["_source"]

    @backoff.on_exception(backoff.expo, ConnectionError, max_time=10, factor=2)
    async def search_data(self, query=None, index=None, size=50, number=None):
        body = query or {"query": {"match_all": {}}}

        data = await self.elasticsearch.search(
            body=body,
            index=index,
            size=size,
            from_=size * number - size if number else None
        )
        return [item["_source"] for item in data["hits"]["hits"]]
