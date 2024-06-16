from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime as dt
import enum


class Role(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_USER = "super"
    


class UserOrm(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    date_of_birth: Mapped[dt.date]
    role: Mapped[Role]
    created_at: Mapped[dt.datetime]
