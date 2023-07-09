from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import WriteOnlyMapped, relationship

from src.db.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    categories: WriteOnlyMapped[list['Category']] = relationship()
    # notes: WriteOnlyMapped[list['Note']] = relationship()
