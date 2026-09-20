

from typing import Annotated
from fastapi import HTTPException, status, Depends, Header
from app.core.security import decode_token
from app.repositories.user_repository import UserRepository
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dbsession import async_get_db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.services.role_permission_service import RolePermissionService
from app.repositories.role_permission_repository import RolePermissionRepository

from app.models.models import Users



security = HTTPBearer()



async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(async_get_db),
):
    repo = UserRepository(db)

    token = credentials.credentials

    decoded_token = decode_token(token)
    email = decoded_token.get('email')

    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token payload')

    user = await repo.get_by_email(email)

    if user:
        return user

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not active')



def require_permission(codename: str):
    async def _check(
        current_user: Users = Depends(get_current_user),
        db: AsyncSession = Depends(async_get_db),
    ):
        # Получаем права пользователя через его роль
        # Если у пользователя нет роли или нет нужного права — raise 403
        
        if not current_user.role:
            raise HTTPException(status_code=403, detail="No role assigned")
        
        # Проверяем, есть ли у роли текущего пользователя нужное право
        repo = RolePermissionRepository(db)
        permissions = await repo.get_permissions_for_role(current_user.role_id)

        if not any(p.codename == codename for p in permissions):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return _check






