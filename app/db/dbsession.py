from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.db.db_connect import Connect
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

connect = Connect()

async_engine = create_async_engine(
    connect.get_connection_url(),
    echo = False
)

AsyncSessionLocal = async_sessionmaker[AsyncSession](async_engine, expire_on_commit=False)

async def async_get_db():
    async with AsyncSessionLocal() as session:
        yield session


