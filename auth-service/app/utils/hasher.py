from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:

    @staticmethod
    def hash_password(password: str) -> str:
        hashed_password = pwd_context.hash(password)
        return hashed_password

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)
