
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Users
from sqlalchemy import  select, delete, update

from app.schemas.users import UserUpdate

class UserRepository:

    def __init__(self, db:AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> Users | None:
        stmt = select(Users).where(Users.email == email)
        user = await self.db.scalar(stmt)
        return user


    async def get_by_id(self, user_id: int) -> Users | None:
        stmt = select(Users).where(Users.id == user_id)
        user = await self.db.scalar(stmt)
        return user


    async def create(self, user_data: dict) -> Users:
        new_user = Users(**user_data)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user


    async def update_user(self, user_id: int, update_data: UserUpdate) -> Users |None:
        update_dict = update_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None

        stmt = update(Users).where(Users.id == user_id).values(update_dict).returning(Users)
        result = await self.db.execute(stmt)
        print(result)
        update_user = result.scalar()
        if update_user:
            await self.db.commit()
            return  update_user

        return None



    async def soft_delete(self, user_id: int) -> bool:

        stmt = select(Users).where(Users.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            user.is_active = False
            await self.db.commit()
            return  True

        return  False







