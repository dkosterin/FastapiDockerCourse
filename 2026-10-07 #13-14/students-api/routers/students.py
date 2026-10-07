from fastapi import APIRouter, Depends, HTTPException
from schemas.students import StudentResponse, StudentCreate
from services.student_service import student_service
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_current_user, require_admin

router = APIRouter(prefix="/students", tags=["students"])

# Depends это встроенный механизм внедрения зависимостей 
# (Dependency Injection, DI)

@router.get("/", response_model=list[StudentResponse])
async def get_students(course: int | None = None, 
                       current_user = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)
                       ) -> list[StudentResponse]:
    return await student_service.get_all_students(db, course)

@router.get("/{id}", response_model=StudentResponse)
async def get_student_by_id(id: int, 
                            current_user = Depends(get_current_user),
                            db: AsyncSession = Depends(get_db)
                            ) -> StudentResponse:
    return await student_service.get_student_by_id(db, id)

@router.post("/", response_model=StudentResponse)
async def add_student(student: StudentCreate, 
                      current_user = Depends(require_admin),
                      db: AsyncSession = Depends(get_db)
                      ) -> StudentResponse:
    return await student_service.append_student(db, student)

@router.put("/{id}", response_model=StudentResponse)
async def update_student_by_id(id: int, 
                               student: StudentCreate, 
                               current_user = Depends(require_admin),
                               db: AsyncSession = Depends(get_db)
                               ) -> StudentResponse:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, 
                             detail="Недостаточно прав")
    return await student_service.update_student_by_id(db, id, student)

@router.delete("/{id}", status_code=204)
async def delete_student(id: int, 
                         current_user = Depends(require_admin),
                         db: AsyncSession = Depends(get_db)
                         ) -> None:
    if current_user.role != "admin":
            raise HTTPException(status_code=403, 
                                 detail="Недостаточно прав")
    await student_service.delete_student_by_id(db, id)