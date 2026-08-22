
from typing import List
from app.models.models import Permissions, Role, Users, RolePermissions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete



class RolePermissionRepository:

    def __init__(self, db:AsyncSession):
        self.db = db


    async def add_permission_to_role(self, role_id: int, permission_id: int) -> None:

        stmt = select(RolePermissions).where(RolePermissions.role_id == role_id, RolePermissions.permission_id == permission_id)
        role_permissions = await self.db.execute(stmt)
        result = role_permissions.scalar_one_or_none()

        if result:
            return result
        
        new_role_permissions = RolePermissions(role_id=role_id, permission_id = permission_id)
        self.db.add(new_role_permissions)
        await self.db.commit()
        await self.db.refresh(new_role_permissions)

        return new_role_permissions




    async def remove_permission_from_role(self, role_id: int, permission_id: int) -> None:
        stmt = select(RolePermissions).where(RolePermissions.role_id == role_id, RolePermissions.permission_id == permission_id)
        role_permission = await self.db.execute(stmt)

        if role_permission.scalar_one_or_none() is not None:
            role_permission_del = delete(RolePermissions).where(RolePermissions.role_id == role_id, RolePermissions.permission_id == permission_id)
            await self.db.execute(role_permission_del)
            await self.db.commit()
            return True
        
        return False



    async def get_permissions_for_role(self, role_id: int) -> List[Permissions]:
        permission_stmt = select(Permissions).join(RolePermissions).where(RolePermissions.role_id == role_id)
        permissions = await self.db.execute(permission_stmt)
        return permissions.scalars().all()

