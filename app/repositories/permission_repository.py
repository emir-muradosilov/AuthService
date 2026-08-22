from typing import List
from app.models.models import Permissions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, exists, update



class PermissionRepository:

    def __init__(self, db:AsyncSession):
        self.db = db


    async def get_all_permissions(self) -> List[Permissions]:
        stmt = select(Permissions)
        all_permissions = await self.db.execute(stmt)
        return all_permissions.scalars().all()


    async def get_permission_by_id(self, perm_id: int) -> Permissions | None:
        stmt = select(Permissions).where(Permissions.id == perm_id)
        permission = await self.db.execute(stmt)
        return permission.scalar_one_or_none()


    async def get_permission_by_codename(self, codename: str) -> Permissions | None:
        stmt = select(Permissions).where(Permissions.codename == codename)
        permission = await self.db.execute(stmt)
        return permission.scalar_one_or_none()


    async def create_permission(self, codename: str, description: str) -> Permissions:
        new_permission = Permissions(codename = codename, description = description)
        self.db.add(new_permission)
        await self.db.commit()
        await self.db.refresh(new_permission)
        return new_permission



    async def update_permission(self, perm_id: int, codename: str, description: str) -> Permissions | None:

        permission = await self.get_permission_by_id(perm_id)

        if not permission:
            return False
        
        permission.codename = codename
        permission.description = description
        await self.db.commit()
        return permission




    async def delete_permission(self, perm_id: int) -> bool:

        stmt = select(Permissions).where(Permissions.id == perm_id)
        delete_permission = await self.db.execute(stmt)

        if delete_permission.scalar_one_or_none() is None:
            return False
        
        delete_perm = delete(Permissions).where(Permissions.id == perm_id)
        await self.db.execute(delete_perm)
        await self.db.commit()

        return True






