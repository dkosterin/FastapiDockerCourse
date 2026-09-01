from fastapi import APIRouter, HTTPException
from schemas.students import StudentResponse, StudentCreate
from services.student_service import student_service, StudentNotFoundException

student_router = APIRouter(prefix="/students", tags=["students"])

@student_router.get("/")
def get_students(course: int | None=None) -> list[StudentResponse]:
    return student_service.get_all_students(course)

@student_router.get("/{id}")
def get_student_by_id(id: int) -> StudentResponse:
    try:
        return student_service.get_student_by_id(id)
    except StudentNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@student_router.post("/")
def add_student(student: StudentCreate) -> StudentResponse:
    return student_service.append_student(student)

@student_router.put("/{id}")
def update_student_by_id(id: int, student: StudentCreate) -> StudentResponse:
    try:
        return student_service.update_student_by_id(id, student)
    except StudentNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@student_router.delete("/{id}", status_code=204)
def delete_student(id: int) -> None:
    try:
        student_service.delete_student_by_id(id)
    except StudentNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))