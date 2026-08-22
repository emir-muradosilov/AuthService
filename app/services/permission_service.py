from app.repositories.permission_repository import PermissionRepository


class PermissionService:

    def __init__(self, repo : PermissionRepository):
        self.repo = repo


    async def create_permission(self, codename: str, description: str):
        permission = await self.repo.create_permission(codename = codename, description = description)
        return permission


    async def get_all_permission(self):
        permissions = await self.repo.get_all_permissions()
        return permissions


    async def get_permission_by_id(self, perm_id: int):
        permission = await self.repo.get_permission_by_id(perm_id=perm_id)
        return permission


    async def get_permission_by_codename(self, codename:str):
        permission = await self.repo.get_permission_by_codename(codename=codename)
        return permission


    async def update_permission(self, perm_id: int, codename: str, description: str):
        permission = await self.repo.update_permission(perm_id=perm_id, codename=codename, description=description)
        return permission


    async def delete_permission(self, perm_id: int):
        permission = await self.repo.delete_permission(perm_id= perm_id)
        return permission


