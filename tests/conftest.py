import asyncio
from typing import Generator

import pytest
from httpx import AsyncClient

from src.db.database import Base, engine
from src.main import app


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True, scope='session')
async def register_two_users():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(url='/auth/register',
                      json={
                          "email": "user@example.com",
                          "password": "pass"
                      }
                      )
        await ac.post(url='/auth/register',
                      json={
                          "email": "user1@example.com",
                          "password": "pass"
                      }
                      )


async def login(username: str, ac: AsyncClient):
    response = await ac.post(url='/auth/jwt/login',
                             data={
                                 "username": username,
                                 "password": "pass"
                             }
                             )
    token = response.cookies.get('fastapiusersauth')
    return token


@pytest.fixture(scope='session')
async def unauthorized_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope='session')
async def authorized_client_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        token = await login(username="user@example.com", ac=ac)
        ac.cookies.set('fastapiusersauth', token)
        yield ac


@pytest.fixture(scope='session')
async def authorized_client_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        token = await login(username="user1@example.com", ac=ac)
        ac.cookies.set('fastapiusersauth', token)
        yield ac


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
