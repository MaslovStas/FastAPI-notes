from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config import settings
from src.db.database import Base, engine
from src.router import router

app = FastAPI(title=settings.PROJECT_NAME,
              openapi_url=f'{settings.API_V1_STR}/openapi.json')

# Set all CORS enabled origins
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
        allow_headers=['*'],
    )

app.include_router(router)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.on_event('startup')
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # await conn.run_sync(Base.metadata.drop_all)
