from functools import lru_cache
from typing import Optional

from aioredis import Redis
from db.cache import CacheBase, CacheService, get_cache
from db.elastic import ElasticBase, ElasticService, get_elastic
from elasticsearch import AsyncElasticsearch
from models.film import MOVIES_INDEX_ELASTIC, Film
from services.base import DetailView, ListView

from fastapi import Depends


class FilmService(ListView, DetailView):
    index = MOVIES_INDEX_ELASTIC
    model = Film

    def _get_key(self, query_search, sort, filter_genre, page_size, page_number) -> Optional[str]:
        return "query_search: %s, sort:%s, filter_genre:%s, page_size:%s, page_number:%s" \
               % (query_search, sort, filter_genre, page_size, page_number)

    def _get_search_request(self, query_search: str = None, sort: str = None,
                            filter_genre: str = None) -> Optional[dict]:
        if query_search:
            body = {
                "query": {
                    "multi_match": {
                        "query": query_search,
                        "fuzziness": "auto",
                        "fields": [
                            "title",
                            "description",
                            "genre.name",
                            "actors_names",
                            "writers_names",
                        ]
                    }
                }
            }
        else:
            body = {"sort": [{"imdb_rating": "asc"}]}
        if sort:
            if sort == "-imdb_rating":
                body["sort"] = [{"imdb_rating": "desc"}]

        if filter_genre:
            body["query"] = {
                "nested": {
                    "path": "genre",
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "match": {
                                        "genre.id": filter_genre
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        return body


@lru_cache()
def get_film_service(
        cache: Redis = Depends(get_cache),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(CacheService(cache), ElasticService(elastic))
