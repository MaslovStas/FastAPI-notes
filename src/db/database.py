from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, as_declarative, declared_attr

from src.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@as_declarative()
class Base:
    id: Mapped[int] = mapped_column(primary_key=True)  # TODO: check index

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}>'
