from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.exception.handler.registers import value_error_handler, permission_error_handler
from Infrastructure.config.database import create_db_and_tables
from web.route.oauth_socials import auth_router
from web.route.files import file_router
from web.route.feed_likes import feed_like_router
from web.route.feeds import feed_router
from web.route.members import member_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # 앱 종료 시 실행 (자원정리 등)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "X-Requested-With"
    ],
)

app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(PermissionError, permission_error_handler)
# app.add_exception_handler(FileNotFoundError, file_not_found_error_handler)

app.include_router(member_router)
app.include_router(feed_router)
app.include_router(feed_like_router)
app.include_router(file_router)
app.include_router(auth_router)
