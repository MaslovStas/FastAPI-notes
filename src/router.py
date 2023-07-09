from fastapi import APIRouter

from src.auth.backend import fastapi_users, auth_backend
from src.auth.schemas import UserRead, UserUpdate, UserCreate
from src.category.router import router as router_category
from src.notes.router import router as router_notes

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(router_category,
                      prefix='/categories',
                      tags=['categories'])

router.include_router(router_notes,
                      prefix='/notes',
                      tags=['notes'])
