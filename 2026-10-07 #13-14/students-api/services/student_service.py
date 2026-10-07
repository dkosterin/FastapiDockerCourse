from schemas.students import StudentCreate
from models.students import StudentDB
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class StudentNotFoundException(Exception):
    pass

# Не очень понятно, какие функции могут быть асинхронными в SQLAlchemy
# Надо гуглить и лезть в документацию
# Если функция обращается в базу данных, то, скорее всего, она асинхронная
# select не асинхрона, потому что select только создает запрос
# open, close, scalars, get, refresh, execute, delete, commit, rollback асинхронные

class StudentService:
    async def get_all_students(self, db: AsyncSession, course: int | None = None) -> list[StudentDB]:
        stmt = select(StudentDB)
        if course is not None:
            stmt = stmt.where(StudentDB.course == course)
        result = await db.scalars(stmt)
        return result.all()


    async def get_student_by_id(self, db: AsyncSession, student_id: int) -> StudentDB:
        student = await db.get(StudentDB, student_id)
        if student is None:
            raise StudentNotFoundException("Студента с таким id нет")
        return student


    async def append_student(self, db: AsyncSession, student: StudentCreate) -> StudentDB:
        new_student = StudentDB(name = student.name, 
                                age=student.age, 
                                course=student.course)
        db.add(new_student)
        await db.commit()
        await db.refresh(new_student)
        return new_student


    async def update_student_by_id(self, 
                             db: AsyncSession,
                             student_id: int, 
                             student: StudentCreate) -> StudentDB:
        existing_student = await self.get_student_by_id(db, student_id)
        existing_student.name = student.name
        existing_student.age = student.age
        existing_student.course = student.course
        await db.commit()
        await db.refresh(existing_student)
        return existing_student

    async def delete_student_by_id(self, db: AsyncSession, student_id: int) -> None:
        existing_student = await self.get_student_by_id(db, student_id)
        await db.delete(existing_student)
        await db.commit()


student_service = StudentService()
        