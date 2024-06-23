import re
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator
import datetime as dt
from app.models.user import Role


NAMING_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z]+$")


class CreateUser(BaseModel):
    email: EmailStr
    name: str
    surname: str
    password: str
    date_of_birth: dt.date

    @field_validator("name", "surname")
    def name_validator(value: str):
        """Проверяет, что выбранные поля содержут
        только символы русского и латинского алфавита,
        а также не являются пустыми.
        """

        if value.isspace():
            raise HTTPException(
                status_code=422, detail=f"Поле {value} не может быть пустым."
            )

        if not NAMING_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail=f"Поле {value} содержит недопустимые символы."
            )
        return value

    @field_validator("password")
    def password_validator(password: str):
        """Проверяет, что пароль:
        состоит из 8+ символов, не состоит из одного символа,
        не состоит из пробелов.
        """
        if len(password) < 8:
            raise HTTPException(status_code=422, detail=f"Пароль слишком короткий")

        if password.count(" ") > 0 or password.isspace():
            raise HTTPException(
                status_code=422, detail=f"Пароль cодержит недопустимые символы"
            )

        symbol = password[0]
        if password.count(symbol) == len(password):
            raise HTTPException(status_code=422, detail=f"Введите пароль надежнее")

        return password

    @field_validator("date_of_birth")
    def date_of_birth_validator(date_of_birth: dt.date):
        current_date = dt.date.today()

        if date_of_birth > current_date:
            raise HTTPException(
                status_code=400,
                detail="Дата рождения не может быть позже чем текущая дата.",
            )

        if abs(int(current_date.year) - int(date_of_birth.year)) >= 115:
            raise HTTPException(status_code=400, detail="Недопустимая дата рождения")
        return date_of_birth


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class GetUser(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    role: Role
    date_of_birth: dt.date


class UpdateUser(BaseModel):
    name: str
    surname: str

    @field_validator("name", "surname")
    def name_validator(value: str):
        """Проверяет, что выбранные поля содержут
        только символы русского и латинского алфавита,
        а также не являются пустыми.
        """

        if value.isspace():
            raise HTTPException(
                status_code=422, detail=f"Поле {value} не может быть пустым."
            )

        if not NAMING_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail=f"Поле {value} содержит недопустимые символы."
            )
        return value
