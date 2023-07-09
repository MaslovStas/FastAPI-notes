from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.category.models import Category
from src.category.scemas import CategoryCreate, CategoryUpdate
from src.db.base_crud import CRUDBase


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    async def get_by_name(self,
                          session: AsyncSession,
                          name: str) -> Category | None:
        return await session.scalar(select(Category).filter_by(name=name))


category_crud = CRUDCategory(Category)
