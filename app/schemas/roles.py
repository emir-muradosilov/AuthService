from pydantic import BaseModel
from typing import Optional, List
from app.schemas.permissions import PermissionResponse

class RoleCreate(BaseModel):
    role_name: str


class RoleUpdate(BaseModel):
    role_name: Optional[str] = None



class RoleResponse(BaseModel):
    id:int
    role_name:str
    permission : Optional[List['PermissionResponse']] = None


    class Config:
        from_attributes = True