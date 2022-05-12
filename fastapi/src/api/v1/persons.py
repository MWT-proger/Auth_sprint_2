from http import HTTPStatus
from typing import Dict, List, Optional, Union

from api import constant
from pydantic import BaseModel
from services.persons import PersonService, get_person_service

from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter()

OBJ_KEY = str
OBJ_VALUE = Optional[Union[float, str]]


class Person(BaseModel):
    id: str
    full_name: str
    films: List[Dict[OBJ_KEY, OBJ_VALUE]] = None


@router.get("/search", response_model=List[Person],
            summary="Поиск персон",
            description="Полнотекстовый поиск персон",
            response_description="Полное имя и список фильмов персоны",
            tags=["Полнотекстовый поиск персон"])
async def persons_search(
        query: Optional[str] = Query(None),
        page_number: int = Query(1, alias="page[number]", title=constant.TITLE_PAGE_NUMBER),
        page_size: int = Query(20, alias="page[size]", title=constant.TITLE_PAGE_SIZE),
        person_service: PersonService = Depends(get_person_service)
) -> List[Person]:
    persons = await person_service.get_specific_data(
        query_search=query,
        page_size=page_size,
        page_number=page_number,
    )
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.PERSONS_NOT_FOUND)
    return [Person.parse_obj(person) for person in persons]


@router.get("/{person_id}", response_model=Person,
            summary="Поиск персоны по id",
            description="Поиск персоны по id",
            response_description="Полное имя и список фильмов персоны",
            tags=["Персона"])
async def person_detail(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.PERSON_NOT_FOUND)
    return Person.parse_obj(person)
