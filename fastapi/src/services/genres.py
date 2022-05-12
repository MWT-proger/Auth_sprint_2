from functools import lru_cache
from typing import Optional

from aioredis import Redis
from db.cache import CacheBase, CacheService, get_cache
from db.elastic import ElasticBase, ElasticService, get_elastic
from elasticsearch import AsyncElasticsearch
from models.genre import GENRES_INDEX_ELASTIC, GENRES_LIST_SIZE, Genre
from services.base import DetailView, ListView

from fastapi import Depends


class GenreService(ListView, DetailView):
    index = GENRES_INDEX_ELASTIC
    model = Genre

    def _get_search_request(self, **kwargs) -> Optional[dict]:
        return None

    def _get_key(self, **kwargs) -> Optional[str]:
        return None


@lru_cache()
def get_genre_service(
        cache: Redis = Depends(get_cache),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreService:
    return GenreService(CacheService(cache), ElasticService(elastic))
