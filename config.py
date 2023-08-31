from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    database_server: str
    database_name: str
    secret_key: str 
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 90

    class Config:
        env_file = ".env"

settings = Settings()
