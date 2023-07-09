from datetime import datetime

from pydantic import BaseModel


class NoteBase(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    category_id: int | None = None
    owner_id: int

    class Config:
        orm_mode = True


class NoteCreate(BaseModel):
    title: str
    content: str | None = None
    category_id: int | None = None


class NoteUpdate(BaseModel):
    title: str | None
    content: str | None
    category_id: int | None
