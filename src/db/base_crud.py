from typing import TypeVar, Generic, Sequence

from pydantic import BaseModel
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import Base

ModelType = TypeVar('ModelType', bound=Base)
SchemaCreateType = TypeVar('SchemaCreateType', bound=BaseModel)
SchemaUpdateType = TypeVar('SchemaUpdateType', bound=BaseModel)


class CRUDBase(Generic[ModelType, SchemaCreateType, SchemaUpdateType]):
    def __init__(self, model: type(ModelType)):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        Parameters
        ----------
        model: A SQLAlchemy model class
        """
        self.model = model

    async def get(self,
                  session: AsyncSession,
                  pk: int) -> ModelType | None:
        return await session.get(self.model, pk)

    async def get_multi(self,
                        session: AsyncSession,
                        skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        result = await session.scalars(query)
        return result.all()

    async def get_multi_with_owner(self,
                                   session: AsyncSession,
                                   owner_id: int,
                                   skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        query = (select(self.model)
                 .filter_by(owner_id=owner_id).
                 offset(skip).
                 limit(limit))
        result = await session.scalars(query)
        return result.all()

    async def create_with_owner(self,
                                session: AsyncSession,
                                obj_in: SchemaCreateType,
                                owner_id: int) -> ModelType:
        query = (insert(self.model).
                 values(**obj_in.dict(), owner_id=owner_id).
                 returning(self.model))
        new_obj = await session.scalar(query)
        await session.commit()
        return new_obj

    async def update(self,
                     session: AsyncSession,
                     pk: int,
                     obj_in: SchemaUpdateType) -> ModelType:
        query = update(self.model).filter_by(id=pk).values(**obj_in.dict(exclude_unset=True)).returning(self.model)
        up_obj = await session.scalar(query)
        await session.commit()
        return up_obj

    async def remove(self,
                     session: AsyncSession,
                     pk: int) -> ModelType:
        del_obj = await session.get(self.model, pk)
        await session.delete(del_obj)
        await session.commit()
        return del_obj
