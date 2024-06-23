from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.core.config import auth_config
from app.core.repository import UserRepo
from app.core.db import db_manager
import datetime as dt
from jose import jwt, JWTError
from app.schemas.token import TokenData
from app.schemas.user import GetUser
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.hasher import Hasher


class AuthService:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
    SECRET_KEY: str = auth_config.SECRET_KEY
    ALGORITHM: str = auth_config.ALGORITHM

    async def authenticate_user(self, session: AsyncSession, email: str, password: str):
        async with session.begin():
            user_repo = UserRepo(session)
            user = await user_repo.get_user_by_email(email=email)
            if user is None:
                return
            if not Hasher.verify_password(password, user.password):
                return
            return user

    def create_access_token(
        self, data: dict, expires_delta: dt.timedelta | None = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = dt.datetime.now(dt.timezone.utc) + expires_delta
        else:
            expire = dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def verify_access_token(self, token: str, form_data_exception) -> TokenData:

        try:
            payload = jwt.decode(
                token, auth_config.SECRET_KEY, algorithms=self.ALGORITHM
            )
            id: str = payload.get("id")
            if id is None:
                raise form_data_exception

            token_data = TokenData(id=id)

        except JWTError:
            raise form_data_exception

        return token_data

    async def get_current_user(
        self,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_manager.get_async_session),
    ) -> GetUser:
        """
        Call this method allows you to get current user by verifying the token,
        and as dependency makes endpoint protected.\n
        Args:\n
        token (str): auth token. example "eyJhbGciOiJIUzI1Ni....AsdEWQ"\n
        session (AsyncSession): Database session.\n
        Raises:\n
        HTTPException: HTTP_401_UNAUTHORIZED.\n
        Returns:\n
        Validated UserModer

        """

        async with session.begin():

            form_data_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not valid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

            token = await self.verify_access_token(token, form_data_exception)
            user_repo = UserRepo(session)
            user = await user_repo.get_user(token.id)
            return GetUser.model_validate(user, from_attributes=True)
