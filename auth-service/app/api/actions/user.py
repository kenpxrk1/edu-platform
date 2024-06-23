from pydantic import EmailStr
from app.core.repository import UserRepo
from app.schemas.user import GetUser, CreateUser, UpdateUser, LoginUser
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.hasher import Hasher
from fastapi import HTTPException


class UserService:

    async def create_user(self, data: CreateUser, session: AsyncSession) -> GetUser:
        async with session.begin():
            data = data.model_dump()
            data["password"] = Hasher.hash_password(data["password"])
            user_repo = UserRepo(session)
            user = await user_repo.create_user(user_data=data)
            return GetUser.model_validate(user, from_attributes=True)

    async def get_users(self, session: AsyncSession) -> list[GetUser]:
        async with session.begin():
            user_repo = UserRepo(session)
            users_data = await user_repo.get_users()
            if users_data is None:
                return []
            return [
                GetUser.model_validate(user, from_attributes=True)
                for user in users_data
            ]

    async def get_user_by_id(self, id: int, session: AsyncSession) -> GetUser:
        async with session.begin():
            user_repo = UserRepo(session=session)
            user_data = await user_repo.get_user(user_id=id)
            if user_data is None:
                raise HTTPException(
                    status_code=404, detail=f"User with id: {id} has not found"
                )
            user = GetUser.model_validate(user_data, from_attributes=True)
            return user

    async def get_user_by_email(
        self, email: EmailStr, session: AsyncSession
    ) -> GetUser:
        async with session.begin():
            user_repo = UserRepo(session)
            user_data = await user_repo.get_user_by_email(email=email)
            if user_data is None:
                raise HTTPException(
                    status_code=404, detail=f"User with id: {email} has not found"
                )
            user = GetUser.model_validate(user_data, from_attributes=True)
            return user

    async def update_user(
        self, id: int, data_to_update: UpdateUser, session: AsyncSession
    ) -> GetUser:
        async with session.begin():
            user_repo = UserRepo(session)
            data_to_update = data_to_update.model_dump()
            updated_data = await user_repo.update_user(id=id, user_data=data_to_update)

            user = GetUser.model_validate(updated_data, from_attributes=True)
            return user

    async def delete_user(self, id: int, session: AsyncSession) -> None:
        async with session.begin():
            user_repo = UserRepo(session)
            await user_repo.delete_user(id=id)
