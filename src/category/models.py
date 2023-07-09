from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.db.database import Base


class Category(Base):
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
