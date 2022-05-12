from functools import lru_cache
from typing import Optional

from aioredis import Redis
from db.cache import CacheBase, CacheService, get_cache
from db.elastic import ElasticBase, ElasticService, get_elastic
from elasticsearch import AsyncElasticsearch
from models.person import PERSON_INDEX_ELASTIC, Person
from services.base import DetailView, ListView

from fastapi import Depends


class PersonService(ListView, DetailView):
    index = PERSON_INDEX_ELASTIC
    model = Person

    def _get_search_request(self, query_search=None, **kwargs) -> Optional[dict]:
        return {"query": {"multi_match": {"query": query_search, "fuzziness": "auto", "fields": ["full_name"]}}} \
            if query_search else None

    def _get_key(self, query_search, page_size, page_number, **kwargs) -> Optional[str]:
        return "query_search: %s, page_size:%s, page_number:%s" \
               % (query_search, page_size, page_number)


@lru_cache()
def get_person_service(
        cache: Redis = Depends(get_cache),
        elasticsearch: AsyncElasticsearch = Depends(get_elastic)
) -> PersonService:
    return PersonService(CacheService(cache), ElasticService(elasticsearch))
