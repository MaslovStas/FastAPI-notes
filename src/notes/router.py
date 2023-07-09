from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.backend import current_user
from src.auth.models import User
from src.category.router import get_category_or_404_or_403
from src.db.database import get_async_session
from src.notes.crud import note_crud
from src.notes.models import Note
from src.notes.scemas import NoteBase, NoteCreate

router = APIRouter()


async def get_note_or_404_or_403(note_id: int,
                                 owner_id: int,
                                 session: AsyncSession) -> Note:
    note = await note_crud.get(session=session, pk=note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Note not found')
    if note.owner_id != owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Access denied')
    return note


@router.get('', response_model=list[NoteBase])
async def get_notes(category_id: int | None = None,
                    user: User = Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)):
    if category_id is not None:
        await get_category_or_404_or_403(cat_id=category_id,
                                         owner_id=user.id,
                                         session=session)
        notes = await note_crud.get_multi_by_category(session=session, cat_id=category_id)
    else:
        notes = await note_crud.get_multi_with_owner(session=session,
                                                     owner_id=user.id,
                                                     skip=0, limit=10)
    return notes


@router.get('/{note_id}', response_model=NoteBase)
async def get_note(note_id: int,
                   user: User = Depends(current_user),
                   session: AsyncSession = Depends(get_async_session)):
    note = await get_note_or_404_or_403(note_id=note_id, owner_id=user.id, session=session)
    return note


@router.post('', status_code=status.HTTP_201_CREATED, response_model=NoteBase)
async def create_note(note_in: NoteCreate,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    new_note = await note_crud.create_with_owner(session=session,
                                                 obj_in=note_in,
                                                 owner_id=user.id)
    return new_note


@router.put('/{note_id}', response_model=NoteBase)
async def update_note(note_id: int,
                      note_in: NoteCreate,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    await get_note_or_404_or_403(note_id=note_id, owner_id=user.id, session=session)
    note = await note_crud.update(session=session,
                                  pk=note_id,
                                  obj_in=note_in)
    return note


@router.delete('/{note_id}', response_model=NoteBase)
async def delete_note(note_id: int,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    await get_note_or_404_or_403(note_id=note_id, owner_id=user.id, session=session)
    note = await note_crud.remove(session=session, pk=note_id)
    return note
