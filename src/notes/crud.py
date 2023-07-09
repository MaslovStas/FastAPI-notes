from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base_crud import CRUDBase
from src.notes.models import Note
from src.notes.scemas import NoteCreate, NoteUpdate


class CRUDNote(CRUDBase[Note, NoteCreate, NoteUpdate]):
    async def get_multi_by_category(self,
                                    session: AsyncSession,
                                    cat_id: int) -> Sequence[Note]:
        query = select(Note).filter_by(category_id=cat_id)
        notes = await session.scalars(query)
        return notes.all()


note_crud = CRUDNote(Note)
