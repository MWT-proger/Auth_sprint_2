import aioredis
from api.v1 import films, genres, persons
from core import config
from db import cache, elastic
from elasticsearch import AsyncElasticsearch
from grpc_client import AuthService_pb2_grpc, client

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title="Read-only API для онлайн-кинотеатра",
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    cache.cache = await aioredis.create_redis_pool((config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20)
    elastic.es = AsyncElasticsearch(hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])
    client.stub = AuthService_pb2_grpc.AuthStub(client.channel)


@app.on_event('shutdown')
async def shutdown():
    await cache.cache.close()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films')
app.include_router(genres.router, prefix='/api/v1/genres')
app.include_router(persons.router, prefix='/api/v1/persons')
