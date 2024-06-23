import os
from pydantic_settings import SettingsConfigDict, BaseSettings

ENV_FILE = os.path.join(os.path.dirname(__file__), ".env")


class DBConfig(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    TEST_DB_NAME: str

    @property
    def TEST_DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.TEST_DB_NAME}"

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="allow")


db_config = DBConfig()


class AuthConfig(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def SECRET_KEY(self):
        return self.__SECRET_KEY

    @property
    def ALGORITHM(self):
        return self.__ALGORITHM

    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self):
        return self.__ACCESS_TOKEN_EXPIRE_MINUTES

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="allow")


auth_config = AuthConfig()
