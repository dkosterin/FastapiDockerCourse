from fastapi import APIRouter, HTTPException, Depends
from schemas.students import StudentResponse, StudentCreate
from services.student_service import student_service, StudentNotFoundException
from database import get_db
from sqlalchemy.orm import Session

student_router = APIRouter(prefix="/students", tags=["students"])

# Depends это встроенный механизм внедрения зависимостей 
# (Dependency Injection, DI)

@student_router.get("/", response_model=list[StudentResponse])
def get_students(course: int | None = None, db: Session = Depends(get_db)) -> list[StudentResponse]:
    return student_service.get_all_students(db, course)

@student_router.get("/{id}", response_model=StudentResponse)
def get_student_by_id(id: int, db: Session = Depends(get_db)) -> StudentResponse:
    return student_service.get_student_by_id(db, id)

@student_router.post("/", response_model=StudentResponse)
def add_student(student: StudentCreate, db: Session = Depends(get_db)) -> StudentResponse:
    return student_service.append_student(db, student)

@student_router.put("/{id}", response_model=StudentResponse)
def update_student_by_id(id: int, student: StudentCreate, db: Session = Depends(get_db)) -> StudentResponse:
    return student_service.update_student_by_id(db, id, student)

@student_router.delete("/{id}", status_code=204)
def delete_student(id: int, db: Session = Depends(get_db)) -> None:
    student_service.delete_student_by_id(db, id)