from typing import Dict, List, Optional, Union
from uuid import UUID

from models.new_base_model import NewBaseModel as BaseModel

OBJ_ID = Union[str, str, UUID]
OBJ_NAME = Union[str, str, UUID]

MOVIES_INDEX_ELASTIC = "movies"


class Film(BaseModel):
    imdb_rating: Optional[float] = None
    genre: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None
    title: str
    description: Optional[str] = None
    director: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None
    actors_names: Optional[List[str]] = None
    writers_names: Optional[List[str]] = None
    actors: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None
    writers: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None


class FilmDetail(BaseModel):
    title: str
    imdb_rating: Optional[float] = None
    description: Optional[str] = None
    genre: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None
    actors: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None
    writers: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None
    directors: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None


class FilmList(BaseModel):
    title: str
    imdb_rating: Optional[float] = None
