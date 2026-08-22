from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.roles import RoleCreate,RoleUpdate,RoleResponse
from app.services.role_service import RoleService
from app.repositories.role_repository import RoleRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dbsession import async_get_db
from app.schemas.permissions import PermissionResponse, PermissionCreate, PermissionUpdate
from app.services.permission_service import PermissionService
from app.repositories.permission_repository import PermissionRepository
from app.api.dependencies import require_permission
from app.schemas.roles import RoleCreate,RoleUpdate,RoleResponse



router = APIRouter(prefix='/admin', tags=['Admin'])




# Role

@router.post('/roles', operation_id="create_role_admin")
async def create_role(role_date:RoleCreate, db:AsyncSession=Depends(async_get_db)):

    repo = RoleRepository(db)
    service = RoleService(repo=repo)

    new_role = await service.create_role(role_date)

    if new_role:
        return new_role
    
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Role already exists')



@router.put('/roles/{role_id}')
async def update_role(role_id:int, role_date:RoleUpdate, db:AsyncSession=Depends(async_get_db)):

    repo = RoleRepository(db)
    service = RoleService(repo=repo)

    new_role = await service.update_role(role_id=role_id, role_name=role_date.role_name)

    if new_role:
        return new_role
    
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect date') 



@router.delete('/roles/{role_id}')
async def delete_role(role_id:int, db:AsyncSession=Depends(async_get_db)):

    repo = RoleRepository(db)
    service = RoleService(repo=repo)

    new_role = await service.delete_role(role_id=role_id)

    if new_role:
        return new_role
    
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect date') 




@router.get('/roles/{role_id}')
async def get_one_role(role_id:int, db:AsyncSession=Depends(async_get_db)):

    repo = RoleRepository(db)
    service = RoleService(repo=repo)

    new_role = await service.get_by_id(role_id=role_id)

    if new_role:
        return new_role
    
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect date') 



@router.get('/roles')
async def get_all_roles(db:AsyncSession=Depends(async_get_db)):
    repo = RoleRepository(db)
    service = RoleService(repo=repo)

    new_role = await service.get_all()

    if new_role:
        return new_role
    
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect date') 




# Permission Rout


@router.post('/permission')
async def create_permission(permission_date:PermissionCreate, db:AsyncSession=Depends(async_get_db)):

    repo = PermissionRepository(db)
    service = PermissionService(repo=repo)

    new_permission = await service.create_permission(codename=permission_date.codename, description=permission_date.description)

    if new_permission:
        return new_permission
    
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Role already exists') 

    

@router.put('/permission/{permission_id}')
async def update_permission(permission_id:int, permission_date:PermissionCreate, db:AsyncSession=Depends(async_get_db)):
    
    repo = PermissionRepository(db)
    service = PermissionService(repo=repo)

    permission = await service.update_permission(perm_id=permission_id, codename=permission_date.codename, description=permission_date.description)

    if permission:
        return permission
    
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect date') 



@router.delete('/permission/{permission_id}')
async def delete_permission(permission_id:int, db:AsyncSession=Depends(async_get_db)):
    
    repo = PermissionRepository(db)
    service = PermissionService(repo=repo)

    permission = await service.delete_permission(perm_id=permission_id)

    if permission:
        return permission
    
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect date') 



@router.get('/permission/{permission_id}')
async def get_one_permission(permission_id:int, db:AsyncSession=Depends(async_get_db)):
    
    repo = PermissionRepository(db)
    service = PermissionService(repo=repo)

    permission = await service.get_permission_by_id(perm_id=permission_id)

    if permission:
        return permission
    
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect date') 



@router.get('/permission')
async def get_all_permissions(db:AsyncSession=Depends(async_get_db)):
    
    repo = PermissionRepository(db)
    service = PermissionService(repo=repo)

    permissions = await service.get_all_permission()

    if permissions:
        return permissions
    
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect date') 




@router.post('/roles', response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    db: AsyncSession = Depends(async_get_db),
    _ = Depends(require_permission("admin:access")),
):
    
    repo = RoleRepository(db)
    service = RoleService(repo=repo)

    existing = await service.get_by_name(role_data.role_name)

    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role already exists")
    
    role = await service.create_role(role_data.role_name)
    return role




@router.get('/roles', response_model=list[RoleResponse])
async def get_roles(
    db: AsyncSession = Depends(async_get_db),
    _ = Depends(require_permission("admin:access")),
):
    repo = RoleRepository(db)
    service = RoleService(repo)
    roles = await service.get_all()
    return roles



@router.get('/roles', response_model=list[RoleResponse])
async def get_role_by_id(
    role_id:int,
    db: AsyncSession = Depends(async_get_db),
    _ = Depends(require_permission("admin:access")),
):
    repo = RoleRepository(db)
    service = RoleService(repo)
    roles = await service.get_by_id(role_id=role_id)
    return roles


@router.get('/roles', response_model=list[RoleResponse])
async def update_role(
    role_date:RoleUpdate,
    role_id:int,
    db: AsyncSession = Depends(async_get_db),
    _ = Depends(require_permission("admin:access")),
):
    repo = RoleRepository(db)
    service = RoleService(repo)
    roles = await service.update_role(role_id=role_id, role_name=role_date.role_name)
    return roles



@router.get('/roles', response_model=list[RoleResponse])
async def delete_role(
    role_id:int,
    db: AsyncSession = Depends(async_get_db),
    _ = Depends(require_permission("admin:access")),
):
    repo = RoleRepository(db)
    service = RoleService(repo)
    roles = await service.delete_role(role_id=role_id)
    return roles






