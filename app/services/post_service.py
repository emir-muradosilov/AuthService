from app.repositories.post_repositiry import PostRepository
from app.schemas.posts import PostCreate, PostUpdate, PostResponse


class PostService:


    def __init__(self, db:PostRepository):
        self.db = db


    async def create_post(self, date:PostCreate, author_id:int):
        new_post = await self.db.create_post(date, author_id)
        return new_post

    async def update_post(self, date:PostUpdate):
        post = await self.db.update_post(date.id, date)
        return post


    async def delete_post(self, id:int):
        result = await self.db.delete_post(id)
        return result


    async def get_all_posts(self):
        posts = await self.db.get_all_posts()
        return posts


    async def get_post_by_post_id(self, post_id:int):
        post = await self.db.get_post_by_id(post_id=post_id)
        return post


    async def get_posts_by_user_id(self, user_id:int):
        posts = await self.db.get_posts_by_user_id(author_id=user_id)
        return posts


