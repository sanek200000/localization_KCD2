from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class SubsOrm(Base):
    __tablename__ = "subs"

    id: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(String(15), unique=True)
