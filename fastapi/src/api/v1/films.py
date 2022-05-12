from http import HTTPStatus
from typing import List, Optional

from api import constant
from models.film import FilmDetail, FilmList
from services.films import FilmService, get_film_service

from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter()


@router.get("/{film_id}", response_model=FilmDetail,
            summary="Поиск кинопроизведения по id",
            description="Поиск кинопроизведениям по id",
            response_description="Название, рейтинг, описание, список жанров и актерский состав фильма",
            tags=["Фильм"]
            )
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmDetail:
    """ Возвращает информацию по фильму с указанным id """
    film = await film_service.get_by_id(film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.FILM_NOT_FOUND)

    return FilmDetail.parse_obj(film)


@router.get("/", response_model=List[FilmList],
            summary="Список кинопроизведений",
            response_description="Название и рейтинг фильма",
            tags=['Фильмы']
            )
async def film_list(sort: Optional[str] = Query(None, alias="sort"),
                    filter_genre: Optional[str] = Query(None, alias="filter[genre]"),
                    page_number: int = Query(1, alias="page[number]", title=constant.TITLE_PAGE_NUMBER),
                    page_size: int = Query(50, alias="page[size]", title=constant.TITLE_PAGE_SIZE),
                    film_service: FilmService = Depends(get_film_service)) -> List[FilmList]:
    """ Возвращает информацию по фильмам"""
    films = await film_service.get_specific_data(
        sort=sort,
        filter_genre=filter_genre,
        page_size=page_size,
        page_number=page_number
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.FILMS_NOT_FOUND)
    return [FilmList.parse_obj(film) for film in films]


@router.get("/search/", response_model=List[FilmList],
            summary="Поиск кинопроизведений",
            description="Полнотекстовый поиск по кинопроизведениям",
            response_description="Название и рейтинг фильма",
            tags=["Полнотекстовый поиск фильмов"]
            )
async def film_list_search(query: Optional[str] = Query(None, alias="query"),
                           page_number: int = Query(1, alias="page[number]", title=constant.TITLE_PAGE_NUMBER),
                           page_size: int = Query(50, alias="page[size]", title=constant.TITLE_PAGE_SIZE),
                           film_service: FilmService = Depends(get_film_service)) -> List[FilmList]:
    """ Возвращает информацию по фильмам"""
    films = await film_service.get_specific_data(
        query_search=query,
        page_size=page_size,
        page_number=page_number
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.FILMS_NOT_FOUND)
    return [FilmList.parse_obj(film) for film in films]
