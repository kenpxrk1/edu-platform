from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import ScalarResult, select, insert, update, delete
from app.models.user import UserOrm


class UserRepo():
    """ Репозиторий для инкапсуляции доступа к данным сервиса авторизации 
        params: session: AsyncSession
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.model = UserOrm

    async def create_user(self, user_data: dict) -> None:
        # try:
        insert_query = insert(self.model).values(**user_data)
        await self.session.execute(insert_query)
        await self.session.commit()
        # except IntegrityError:
        #     raise HTTPException(
        #             status_code=400, detail=f"Пользователь с таким адресом уже существует"
        #         )

    
    async def get_user(self, user_id: int) -> ScalarResult | None:
        select_query = select(self.model).where(self.model.id == user_id)
        user = await self.session.execute(select_query)
        return user.scalar_one_or_none()
    

    async def get_users(self) -> tuple | None:
        select_query = select(self.model)
        users = await self.session.execute(select_query)
        return users.scalars().all()
    
    
    async def get_user_by_email(self, email: str) -> ScalarResult | None:
        select_query = select(self.model).where(self.model.email == email)
        user = await self.session.execute(select_query)
        return user.scalar_one_or_none()
    

    async def update_user(self, id: int, user_data: dict) -> ScalarResult:
        select_query = select(UserOrm).where(UserOrm.id == id)
        result = await self.session.execute(select_query)
        if result.scalar_one_or_none is None:
            raise HTTPException(
                status_code=400, detail="Пользователь с id: {id} не найден, операция не возможна."
            )
        update_query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**user_data)
            .returning(self.model)
        )
        updated_user = await self.session.execute(update_query)
        await self.session.commit()
        return updated_user.scalar_one()
    

    async def delete_user(self, id: int) -> None:
        select_query = select(UserOrm).where(UserOrm.id == id)
        result = await self.session.execute(select_query)
        if result.scalar_one_or_none is None:
            raise HTTPException(
                status_code=400, detail="Пользователь с id: {id} не найден, операция не возможна."
            )
        delete_query = (
            delete(self.model).where(self.model.id == id)
        )
        await self.session.execute(delete_query)
        await self.session.commit()
    

    