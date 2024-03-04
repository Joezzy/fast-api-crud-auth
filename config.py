from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_POST: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM:  str
    ACCESS_TOKEN_EXPIRRY: int

    class Config:
        env_file=".env"

settings=Settings();

# print(settings.DATSBASE_PASSWORD)