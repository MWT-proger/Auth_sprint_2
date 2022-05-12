from http import HTTPStatus
from typing import List

from api import constant
from grpc_client.dependencies import get_role
from pydantic import BaseModel
from services.genres import GenreService, get_genre_service

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


class Genre(BaseModel):
    id: str
    name: str


@router.get("/{genre_id}", response_model=Genre,
            summary="Поиск жанра по id",
            description="Поиск жанра по id",
            response_description="Название жанра",
            tags=["Жанр"])
async def genre_detail(genre_id: str,
                       genre_service: GenreService = Depends(get_genre_service),
                       roles: str = Depends(get_role)) -> Genre:

    print(roles)
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.GENRE_NOT_FOUND)
    return Genre(id=genre.id, name=genre.name)


@router.get("/", response_model=List[Genre],
            summary="Список жанров",
            description="Список жанров",
            response_description="Название жанра",
            tags=["Жанры"])
async def genre_list(genre_service: GenreService = Depends(get_genre_service)) -> List[Genre]:
    genres = await genre_service.get_specific_data()
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.GENRES_NOT_FOUND)
    return [Genre.parse_obj(genre) for genre in genres]
