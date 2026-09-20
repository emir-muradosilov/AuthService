

from app.db.dbsession import async_get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.role_repository import RoleRepository
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_permission_repository import RolePermissionRepository
from app.services.role_service import RoleService
from app.models.models import Role, RolePermissions, Permissions, Users
from sqlalchemy import select
from app.repositories.user_repository import UserRepository
from fastapi import HTTPException, status





DEFAULT_ROLES = ['user', 'admin']



DEFAULT_PERMISSIONS_USER = {
    "posts:view": "Can view posts",
    "posts:create": "Can create posts",
    "posts:edit": "Can edit own posts",
    "posts:delete": "Can delete own posts",
}

DEFAULT_PERMISSIONS_ADMIN = {
    "admin:access": "Can access admin endpoints",
}



async def init_roles_and_permissions(session: AsyncSession):

    role_repo = RoleRepository(session)

# Проверка и добавление базовых ролей

    for role in DEFAULT_ROLES:
        stmt = select(Role).where(Role.role_name == role)
        new_role = await session.execute(stmt)
        if not new_role.scalar_one_or_none():
            new_role = Role(role_name = role)
            session.add(new_role)


# Добавяление разрешений

    user_permission = await add_permission(session, DEFAULT_PERMISSIONS_USER)
    admin_permission = await add_permission(session, DEFAULT_PERMISSIONS_USER|DEFAULT_PERMISSIONS_ADMIN)


# Добавяление связи базовых ролей с разрешениями в таблице 

    user_role_permission = await add_role_permission(session, role_repo, 'user', DEFAULT_PERMISSIONS_USER)
    admin_role_permission = await add_role_permission(session, role_repo, 'admin', DEFAULT_PERMISSIONS_USER|DEFAULT_PERMISSIONS_ADMIN)



async def add_permission(session:AsyncSession, DEFAULT_PERMISSIONS):

    for permission_k, permission_v in DEFAULT_PERMISSIONS.items():
        stmt = select(Permissions).where(Permissions.codename == permission_k)
        new_permission = await session.execute(stmt)
        if not new_permission.scalar_one_or_none():
            new_permission = Permissions(codename = permission_k, description = permission_v)
            session.add(new_permission)
    await session.commit()



async def add_role_permission(session:AsyncSession, role_repo:RoleRepository, role_name:str, DEFAULT_PERMISSIONS:dict):

    role_rel = await role_repo.get_by_name(role_name)
    if not role_rel:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Role couldt found')
    id_list=[]
    for permission_k, permission_v in DEFAULT_PERMISSIONS.items():
        stmt = select(Permissions).where(Permissions.codename == permission_k)
        res = await session.execute(stmt)
        id_list.append(res.scalar_one_or_none().id)

    for perm_id in id_list:
        stmt = select(RolePermissions).where(RolePermissions.role_id == role_rel.id, RolePermissions.permission_id == perm_id)
        res = await session.execute(stmt)
        if res.scalar_one_or_none():
            continue
        stmt = RolePermissions(role_id = role_rel.id, permission_id = perm_id)
        session.add(stmt)
    await session.commit()





