from typing import Optional

from models.new_base_model import NewBaseModel as BaseModel

GENRES_INDEX_ELASTIC = "genres"
GENRES_LIST_SIZE = 100


class Genre(BaseModel):
    name: str
    description: Optional[str] = None
