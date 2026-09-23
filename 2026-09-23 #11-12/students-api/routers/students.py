from fastapi import APIRouter, Depends
from schemas.students import StudentResponse, StudentCreate
from services.student_service import student_service
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/students", tags=["students"])

# Depends это встроенный механизм внедрения зависимостей 
# (Dependency Injection, DI)

@router.get("/", response_model=list[StudentResponse])
async def get_students(course: int | None = None, db: AsyncSession = Depends(get_db)) -> list[StudentResponse]:
    return await student_service.get_all_students(db, course)

@router.get("/{id}", response_model=StudentResponse)
async def get_student_by_id(id: int, db: AsyncSession = Depends(get_db)) -> StudentResponse:
    return await student_service.get_student_by_id(db, id)

@router.post("/", response_model=StudentResponse)
async def add_student(student: StudentCreate, db: AsyncSession = Depends(get_db)) -> StudentResponse:
    return await student_service.append_student(db, student)

@router.put("/{id}", response_model=StudentResponse)
async def update_student_by_id(id: int, student: StudentCreate, db: AsyncSession = Depends(get_db)) -> StudentResponse:
    return await student_service.update_student_by_id(db, id, student)

@router.delete("/{id}", status_code=204)
async def delete_student(id: int, db: AsyncSession = Depends(get_db)) -> None:
    await student_service.delete_student_by_id(db, id)