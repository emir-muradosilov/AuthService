
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.posts import PostCreate, PostUpdate, PostResponse
from sqlalchemy import select, delete, update
from app.models.models import Post

class PostRepository:


    def __init__(self, db:AsyncSession):
        self.db=db


    async def create_post(self, date:PostCreate, author_id:int):
        new_post = Post(title= date.title, text = date.text, author_id = author_id)
        self.db.add(new_post)
        await self.db.commit()
        await self.db.refresh(new_post)
        return new_post


    async def get_all_posts(self):
        stmt = select(Post)
        all_posts = await self.db.execute(stmt)
        return all_posts.scalars().all()



    async def get_post_by_id(self, post_id:int):
        stmt = select(Post).where(Post.id == post_id)
        post = await self.db.execute(stmt)
        return post.scalar_one_or_none()



    async def get_posts_by_user_id(self, author_id:int):
        stmt = select(Post).where(Post.author_id == author_id)
        posts = await self.db.execute(stmt)
        return posts.scalars().all()



    async def update_post(self, post_id:int, date:PostUpdate):
        post = await self.get_post_by_id(post_id)

        if not post:
            return None

        if date.title is not None:
            post.title = date.title
        if date.text is not None:
            post.text = date.text
        await self.db.commit()
        await self.db.refresh(post)
        return post




    async def delete_post(self, post_id:int):
        post = await self.get_post_by_id(post_id)

        if post is None:
            return False

        stmt = delete(Post).where(Post.id == post_id)
        await self.db.execute(stmt)
        await self.db.commit()

        return True 


