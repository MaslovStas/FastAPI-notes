from datetime import datetime

from pydantic import BaseModel


class CategoryBase(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str
