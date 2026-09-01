from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers.students import student_router
from routers.pages import pages_router

# Архитектура приложения
# schemas
# services
# routers

# https://github.com/dkosterin/FastapiDockerCourse

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
