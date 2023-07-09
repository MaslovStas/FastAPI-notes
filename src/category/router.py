from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.backend import current_user
from src.auth.models import User
from src.category.crud import category_crud
from src.category.scemas import CategoryBase, CategoryCreate
from src.db.database import get_async_session

router = APIRouter()


async def get_category_or_404_or_403(cat_id: int,
                                     owner_id: int,
                                     session: AsyncSession):
    cat = await category_crud.get(session=session, pk=cat_id)
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Category not found')
    if cat.owner_id != owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Access denied')
    return cat


@router.get('', response_model=list[CategoryBase])
async def get_categories(user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    cats = await category_crud.get_multi_with_owner(session=session,
                                                    owner_id=user.id,
                                                    skip=0, limit=10)
    return cats


@router.get('/{cat_id}', response_model=CategoryBase)
async def get_category(cat_id: int,
                       user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    cat = await get_category_or_404_or_403(cat_id=cat_id, owner_id=user.id, session=session)
    return cat


@router.post('', status_code=status.HTTP_201_CREATED, response_model=CategoryBase)
async def create_category(cat_in: CategoryCreate,
                          user: User = Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)):
    existing_cat = await category_crud.get_by_name(session=session,
                                                   name=cat_in.name)
    if existing_cat is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Category with this name already exists')

    new_cat = await category_crud.create_with_owner(session=session,
                                                    obj_in=cat_in,
                                                    owner_id=user.id)
    return new_cat


@router.put('/{cat_id}', response_model=CategoryBase)
async def update_category(cat_id: int,
                          cat_in: CategoryCreate,
                          user: User = Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)):
    await get_category_or_404_or_403(cat_id=cat_id, owner_id=user.id, session=session)
    cat = await category_crud.update(session=session,
                                     pk=cat_id,
                                     obj_in=cat_in)
    return cat


@router.delete('/{cat_id}', response_model=CategoryBase)
async def delete_category(cat_id: int,
                          user: User = Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)):
    await get_category_or_404_or_403(cat_id=cat_id, owner_id=user.id, session=session)
    cat = await category_crud.remove(session=session, pk=cat_id)
    return cat
