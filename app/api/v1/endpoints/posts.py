
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.posts import PostCreate, PostResponse, PostUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dbsession import async_get_db
from app.repositories.post_repositiry import PostRepository
from app.services.post_service import PostService
from app.api.dependencies import require_permission, get_current_user
from app.models.models import Users


router = APIRouter(prefix='/posts', tags=['Posts'])



@router.post('/')
async def create_post(
    date:PostCreate, 
    db:AsyncSession=Depends(async_get_db),
    current_user: Users = Depends(require_permission("posts:create")),
       ):

    repo = PostRepository(db)
    service = PostService(repo)

    user = current_user 

    new_post = await service.create_post(date, user.id)

    if not new_post:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='new post not created. Try leater.')

    return new_post




@router.put('/{post_id}')
async def update_post(date:PostUpdate, db:AsyncSession=Depends(async_get_db), current_user: Users = Depends(require_permission("posts:edit")),):

    repo = PostRepository(db)
    service = PostService(repo)

    updated_post = await service.update_post(date)

    if not updated_post:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='new post not created. Try leater.')

    return updated_post


@router.get('/{post_id}')
async def get_post(post_id:int, db:AsyncSession=Depends(async_get_db), _ = Depends(require_permission("posts:view")),):

    repo = PostRepository(db)
    service = PostService(repo)

    post = await service.get_post_by_post_id(post_id)

    if not post:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='new post not created. Try leater.')

    return post


@router.get('/')
async def get_all_posts(db:AsyncSession=Depends(async_get_db), _ = Depends(require_permission("posts:view")),):

    repo = PostRepository(db)
    service = PostService(repo)

    posts = await service.get_all_posts()

    if not posts:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='new post not created. Try leater.')

    return posts


@router.delete('/{post_id}')
async def delete_post(post_id:int, db:AsyncSession=Depends(async_get_db)):

    repo = PostRepository(db)
    service = PostService(repo)

    new_post = await service.delete_post(post_id)

    if not new_post:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='new post not created. Try leater.')

    return new_post




