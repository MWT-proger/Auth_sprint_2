from datetime import date
from typing import Dict, List, Optional, Union

from models.new_base_model import NewBaseModel as BaseModel

OBJ_KEY = str
OBJ_VALUE = Optional[Union[float, str]]

PERSON_INDEX_ELASTIC = "persons"


class Person(BaseModel):
    full_name: str
    birth_date: Optional[date] = None
    role: List[str] = None
    films: List[Dict[OBJ_KEY, OBJ_VALUE]] = None
