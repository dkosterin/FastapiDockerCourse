from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from routers.students import router as student_router
from routers.pages import pages_router
from routers.auth import router as auth_router
from services.auth_service import AuthException, UserAlreadyExistException
from services.student_service import StudentNotFoundException

# Архитектура приложения
# schemas
# services
# routers

# https://github.com/dkosterin/FastapiDockerCourse

# Base.metadata.create_all(engine)

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

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