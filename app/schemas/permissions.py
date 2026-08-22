
from pydantic import BaseModel
from typing import Optional



class PermissionCreate(BaseModel):
    codename: str
    description:str | None


class PermissionUpdate(BaseModel):
    codename: Optional[str] = None
    description: Optional[str] = None



class PermissionResponse(BaseModel):
    id:int
    codename:str
    description:str | None

    class Config:
        from_attributes = True

