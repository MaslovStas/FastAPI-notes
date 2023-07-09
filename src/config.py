import secrets
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseSettings, AnyHttpUrl, validator, PostgresDsn

load_dotenv()


class Config(BaseSettings):
    PROJECT_NAME: str = 'MyProject'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    API_V1_STR: str = '/api/v1'
    # CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    CORS_ORIGINS: list[AnyHttpUrl] = []

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            path=f"/{values.get('POSTGRES_DB', '')}"
        )

    class Config:
        case_sensitive = True


settings = Config()

# print(json.dumps(settings.dict(), indent=4, sort_keys=False))
