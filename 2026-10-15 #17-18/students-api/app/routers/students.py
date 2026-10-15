from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis
from app.schemas.students import StudentResponse, StudentCreate
from app.services.student_service import student_service
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_user, require_admin, get_redis

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
                            db: AsyncSession = Depends(get_db),
                            redis: Redis = Depends(get_redis)
                            ) -> StudentResponse:
    key = f"student:{id}"
    cached_student = await redis.get(key)
    if cached_student is not None:
         print("Student from cache")
         return StudentResponse.model_validate_json(cached_student)

    student = await student_service.get_student_by_id(db, id)
    student_response = StudentResponse.model_validate(student)
    await redis.set(key, student_response.model_dump_json(), ex=60)
    print("Student added to cache")
    return student_response

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
                               db: AsyncSession = Depends(get_db),
                               redis: Redis = Depends(get_redis)
                               ) -> StudentResponse:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, 
                             detail="Недостаточно прав")
    updated_student = await student_service.update_student_by_id(db, id, student)
    await redis.delete(f"student:{id}")
    return updated_student

@router.delete("/{id}", status_code=204)
async def delete_student(id: int, 
                         current_user = Depends(require_admin),
                         db: AsyncSession = Depends(get_db),
                         redis: Redis = Depends(get_db)
                         ) -> None:
    if current_user.role != "admin":
            raise HTTPException(status_code=403, 
                                 detail="Недостаточно прав")
    await student_service.delete_student_by_id(db, id)
    await redis.delete(f"student:{id}")