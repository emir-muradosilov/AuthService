from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_current_user, require_permission
from app.schemas.users import UserCreate,UserLogin,UserUpdate,UserDelete, UserResponse
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.models.models import Users
from app.db.dbsession import async_get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.repositories.role_repository import RoleRepository





router = APIRouter(prefix = '/auth', tags=["Auth"])


@router.post('/registration',)
async def registration(user_date:UserCreate, db: AsyncSession = Depends(async_get_db)):

    repository = UserRepository(db)
    service = UserService(repo=repository)

    user = await service.registration(user_date)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect user date')

    return user




@router.post('/login', )
async def login(user_date:UserLogin, db: AsyncSession = Depends(async_get_db), ):

    repository = UserRepository(db)
    service = UserService(repo=repository)

    token = await service.login(user_date)

    if token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect user date')

    return token



@router.put('/{user_id}', )
async def update(
        user_id:int,
        user_date:UserUpdate,
        db:AsyncSession = Depends(async_get_db),
        user = Depends(get_current_user),
):
    if user_id == user.id:
        repository = UserRepository(db)
        service = UserService(repo=repository)

        user_update = await service.update_profile(user.id, user_date)

        if user_update is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can only update your own profile')

        return True

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User not found or no changes made')



@router.delete('/users/{user_id}', )
async def delete(
        user_id:int,
        db:AsyncSession = Depends(async_get_db),
        user = Depends(get_current_user),
):

    if user_id == user.id:

        repository = UserRepository(db)
        service = UserService(repo=repository)

        delete_user = await service.delete_user(user.id)

        if delete_user is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Incorrect user date')

        return True

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can only update your own profile')



@router.post('/users/{user_id}/role/{role_id}')
async def assign_role_to_user(
    user_id: int,
    role_id: int,
    db: AsyncSession = Depends(async_get_db),
    current_user = Depends(require_permission("admin:access")),
):
    # Проверить, что пользователь и роль существуют
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    role_repo = RoleRepository(db)
    role = await role_repo.get_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Назначить роль
    user.role_id = role_id
    await db.commit()
    return {"message": f"Role {role_id} assigned to user {user_id}"}



