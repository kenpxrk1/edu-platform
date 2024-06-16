from pydantic import BaseModel


class DBConfig(BaseModel):
    __DB_HOST: str
    __DB_PORT: str
    __DB_USER: str
    __DB_PASS: str
    __DB_NAME: str 

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.__DB_USER}:{self.__DB_PASS}@{self.__DB_HOST}:{self.__DB_PORT}/{self.__DB_NAME}"


db_config = DBConfig()


class AuthConfig(BaseModel):
    __SECRET_KEY: str
    __ALGORITHM: str
    __ACCESS_TOKEN_EXPIRE_MINUTES: int 

    @property
    def SECRET_KEY(self):
        return self.__SECRET_KEY
    
    @property
    def ALGORITHM(self):
        return self.__ALGORITHM
    
    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self):
        return self.__ACCESS_TOKEN_EXPIRE_MINUTES
