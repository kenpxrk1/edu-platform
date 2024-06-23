from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.config import db_config
from app.api.crud import router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print(f"Host: {db_config.DB_HOST}")
#     print(f"Port: {db_config.DB_PORT}")
#     print(f"User: {db_config.DB_USER}")
#     print(f"Pass: {db_config.DB_PASS}")
#     print(f"Name: {db_config.DB_NAME}")
#     print(f"URL: {db_config.DB_URL}")
#     yield
    

app = FastAPI(lifespan=lifespan)

app.include_router(router=router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)