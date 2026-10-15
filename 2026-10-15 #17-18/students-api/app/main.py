from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.routers.students import router as student_router
from app.routers.pages import pages_router
from app.routers.auth import router as auth_router
from app.services.auth_service import AuthException, UserAlreadyExistException
from app.services.student_service import StudentNotFoundException
from app.config import settings
from contextlib import asynccontextmanager
import redis.asyncio as redis

# Архитектура приложения
# schemas
# services
# routers

# https://github.com/dkosterin/FastapiDockerCourse

# Base.metadata.create_all(engine)

# 1. Redis
# 2. Деплой

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = redis.Redis.from_url(settings.redis_url,
                                           decode_responses=True
                                        )
    yield 

    await app.state.redis.aclose()

app = FastAPI(lifespan=lifespan)
app.mount('/app/static', StaticFiles(directory='app/static'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", # адрес клиента
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student_router)
app.include_router(pages_router)
app.include_router(auth_router)

@app.exception_handler(StudentNotFoundException)
async def student_not_found_handler(request: Request, exc: StudentNotFoundException) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(UserAlreadyExistException)
async def student_not_found_handler(request: Request, exc: UserAlreadyExistException) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(AuthException)
async def student_not_found_handler(request: Request, exc: UserAlreadyExistException) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": str(exc)})