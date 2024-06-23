from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import EmailStr
from app.schemas.user import GetUser, CreateUser, UpdateUser, LoginUser
from app.schemas.token import Token
from sqlalchemy.ext.asyncio import AsyncSession
from .deps import get_auth_service, get_user_service, auth_service
from .actions.auth import AuthService
from .actions.user import UserService
from app.core.db import db_manager


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[GetUser])
async def get_users(
    session: AsyncSession = Depends(db_manager.get_async_session),
    user_service: UserService = Depends(get_user_service),
    current_user: GetUser = Depends(auth_service.get_current_user)
) -> list[GetUser]:
    """ Возвращает список всех пользователей """
    users = await user_service.get_users(session)
    return users


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: CreateUser,
    session: AsyncSession = Depends(db_manager.get_async_session),
    user_service: UserService = Depends(get_user_service),
) -> None:
    """ Создает нового пользователя в базе данных """
    return await user_service.create_user(
        data=user_data,
        session=session
    )

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(db_manager.get_async_session)
):
    user = await auth_service.authenticate_user(
        email=form_data.username, 
        password=form_data.password, 
        session=session
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )
    token = auth_service.create_access_token(
        data=({"id": str(user.id), "role": user.role}),
        expires_delta=timedelta(minutes=60 * 8),
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/get_user_by_id/{id}", response_model=GetUser, status_code=200)
async def get_user_by_id(
    id: int, 
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(db_manager.get_async_session)
):
    user = await user_service.get_user_by_id(id=id, session=session)
    return user 


@router.get("/get_user_by_email/{email}", response_model=GetUser, status_code=200)
async def get_user_by_email(
    email: EmailStr,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(db_manager.get_async_session)
):
    user = await user_service.get_user_by_email(email=email, session=session)
    return user 


@router.put("/{id}", response_model=GetUser, status_code=status.HTTP_201_CREATED)
async def update_user(
    data_to_update: UpdateUser,
    id: int,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: GetUser = Depends(auth_service.get_current_user)

) -> GetUser:
    
    updated_user = await user_service.update_user(
        id=id, 
        data_to_update=data_to_update,
        session=session
    )

    return updated_user


@router.delete("/{id}", status_code=204)
async def delete_user(
    id: int,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(db_manager.get_async_session),
    current_user: GetUser = Depends(auth_service.get_current_user) 
) -> None:
    return await user_service.delete_user(
        id=id,
        session=session
    )