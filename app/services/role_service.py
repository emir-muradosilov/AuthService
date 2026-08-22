from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.role_repository import RoleRepository


class RoleService:

    def __init__(self, repo:RoleRepository):
        self.repo = repo


    async def create_role(self, name:str):
        role = await self.repo.create_role(payload= name)
        return role


    
    async def update_role(self, role_id:int, role_name:str):
        role = await self.repo.update_role(role_id=role_id, name=role_name)
        return role


    async def delete_role(self, role_id:int):
        result = await self.repo.delete_role(role_id=role_id)
        return result


    async def get_all(self):
        all_role = await self.repo.get_all()
        return all_role


    async def get_by_id(self, role_id:int):
        role = await self.repo.get_by_id(role_id= role_id)
        return role


    async def get_by_name(self, role_name:str):
        role = await self.repo.get_by_name(name=role_name)
        return role