
from pydantic_settings import BaseSettings


class Connect(BaseSettings):

    db_name : str
    db_host : str
    db_port : str
    db_user : str
    db_password : str

    def get_connection_url(self ):

        return f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'

    class Config:
        env_file = '.env'
        env_file_encoding = "utf-8"
        extra = "ignore"