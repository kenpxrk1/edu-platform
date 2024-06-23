from sqlalchemy import text
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime as dt
import enum


class Role(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_USER = "super"
    


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    name: Mapped[str]
    surname: Mapped[str]
    date_of_birth: Mapped[dt.date] 
    role: Mapped[Role] = mapped_column(default=Role.USER)
    created_at: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now())
    is_active: Mapped[bool] = mapped_column(default=False)
