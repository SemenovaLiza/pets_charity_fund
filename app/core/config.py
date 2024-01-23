from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд для котов'
    description: str = 'Сервис для благотворительного фонда котов'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    class Config:
        env_file = '.env'


settings = Settings() 