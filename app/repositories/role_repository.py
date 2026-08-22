from app.models.models import Role, Users
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, exists
from app.schemas.roles import RoleCreate


class RoleRepository:


    def __init__(self, db : AsyncSession):
        self.db = db


    async def get_all(self) -> List[Role]:
        stmt = select(Role)
        all_roles = await self.db.execute(stmt)
        return all_roles.scalars().all()

    

    async def get_by_id(self, role_id: int) -> Role | None:
        stmt = select(Role).where(Role.id == role_id)
        role = await self.db.execute(stmt)
        return role.scalar_one_or_none()
    


    async def get_by_name(self, name: str) -> Role | None:
        stmt = select(Role).where(Role.role_name == name)
        role = await self.db.execute(stmt)
        return role.scalar_one_or_none()



    async def create_role(self, payload: RoleCreate) -> Role:
        new_role = Role(role_name=payload.role_name)
        self.db.add(new_role)
        await self.db.commit()
        await self.db.refresh(new_role)
        return new_role



    async def update_role(self, role_id: int, name: str) -> Role | None:

        role = await self.get_by_id(role_id)

        if not role:
            return None
        
        role.role_name = name
        await self.db.commit()
        await self.db.refresh(role)
        return role





    async def delete_role(self, role_id: int) -> bool:

        stmt = select(Users).where(Users.role_id == role_id)
        result = await self.db.execute(stmt)

        if result.scalar_one_or_none() is not None:
            return False
        
        await self.db.delete(await self.get_by_id(role_id))
        await self.db.commit()

        return True 





