
from app.repositories.user_repository import UserRepository
from app.schemas.users import UserCreate, UserLogin, UserUpdate, UserResponse
from app.core.security import hash_password, verify_password, create_login_token


class UserService:

    def __init__(self, repo:UserRepository):
        self.repo = repo



    async def registration(self, new_user_date:UserCreate):

        user_in_db = await self.repo.get_by_email(new_user_date.email)
        
        if user_in_db:
            return None


        user_dict = new_user_date.model_dump()
        user_password = user_dict.get('password')

        user_dict.pop('password_confirm', None)

        hashed_password = hash_password(user_password)
        user_dict.pop('password', None)
        user_dict['password_hash'] = hashed_password

        result = await self.repo.create(user_data = user_dict)

        return result



    async def login(self, user_date:UserLogin):
        user = await self.repo.get_by_email(user_date.email)

        if not user or not user.is_active:
            return None

        res_pass_verify = verify_password(hashed_password=user.password_hash, plain_password=user_date.password)

        if not res_pass_verify:
                return None

        token = create_login_token(date={'user_name':user.user_name, 'email':user.email})
        return {"access_token": token, "token_type": "bearer"}




    async def update_profile(self, user_id:int, user_update_date:UserUpdate):
        result = await self.repo.update_user(user_id, user_update_date)
        return result



    async def delete_user(self, user_id:int):
        result = await self.repo.soft_delete(user_id)
        return result
