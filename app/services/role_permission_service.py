
from app.repositories.role_permission_repository import RolePermissionRepository
from sqlalchemy.ext.asyncio import AsyncSession




class RolePermissionService():


    def __init__(self, db:RolePermissionRepository):
        self.db = db



    async def get_permissions_for_role(self, role_id:int):
        permissions = await self.db.get_permissions_for_role(role_id=role_id, )
        return permissions