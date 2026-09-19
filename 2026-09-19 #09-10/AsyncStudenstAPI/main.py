from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from routers.students import student_router
from routers.pages import pages_router
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

@app.exception_handler(StudentNotFoundException)
async def student_not_found_handler(request: Request, exc: StudentNotFoundException) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})

# 2. Асинхронность
# 3. Аутентификация и авторизация