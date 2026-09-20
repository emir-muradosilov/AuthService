from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    title : str
    text : str


class PostDelete(BaseModel):
    id:int


class PostUpdate(BaseModel):
    id:int
    title : str | None = None
    text : str | None = None


class PostResponse(BaseModel):
    id: int
    title : str
    text : str
    author_id : int
    created_at : datetime
    updated_at : datetime

    class Config:
        from_attributes = True
