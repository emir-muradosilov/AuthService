import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("SECRET")
algorithm = os.getenv("ALGORITHM")


def hash_password(password:str)->str:
    return bcrypt.hashpw(password=password.encode('utf-8'), salt= bcrypt.gensalt()).decode('utf-8')



def verify_password(hashed_password: str | bytes, plain_password: str | bytes)->bool:
    if isinstance(plain_password, str):
        plain_bytes = plain_password.encode('utf-8')
    else:
        plain_bytes = plain_password

        # 2. Принудительно переводим хэш из БД в bytes, если это строка
    if isinstance(hashed_password, str):
        hash_bytes = hashed_password.encode('utf-8')
    else:
        hash_bytes = hashed_password

        # 3. Передаем в bcrypt гарантированные bytes объекты
    return bcrypt.checkpw(password=plain_bytes, hashed_password=hash_bytes)


def create_login_token(date:dict):

    now = datetime.now(timezone.utc)
    issued_at = int(now.timestamp())
    expire_at = int((now + timedelta(hours=72)).timestamp())

    payload = {
        'sub':date['user_name'],
        'email': date['email'],
        "iat": issued_at,
        "exp": expire_at,
    }

    token = jwt.encode(payload, secret_key, algorithm)

    return token



def decode_token(token):
    decoded_token = jwt.decode(token=token, key=secret_key, algorithms=algorithm)
    return decoded_token