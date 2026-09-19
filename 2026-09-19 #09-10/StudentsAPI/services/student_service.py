from schemas.students import StudentCreate
from models.students import StudentDB
from sqlalchemy import select
from sqlalchemy.orm import Session

class StudentNotFoundException(Exception):
    pass

class StudentService:
    def get_all_students(self, db: Session, course: int | None = None) -> list[StudentDB]:
        stmt = select(StudentDB)
        if course is not None:
            stmt = stmt.where(StudentDB.course == course)
        return db.scalars(stmt).all()


    def get_student_by_id(self, db: Session, student_id: int) -> StudentDB:
        student = db.get(StudentDB, student_id)
        if student is None:
            raise StudentNotFoundException("Студента с таким id нет")
        return student


    def append_student(self, db: Session, student: StudentCreate) -> StudentDB:
        new_student = StudentDB(name = student.name, 
                                age=student.age, 
                                course=student.course)
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student


    def update_student_by_id(self, 
                             db: Session,
                             student_id: int, 
                             student: StudentCreate) -> StudentDB:
        existing_student = self.get_student_by_id(db, student_id)
        existing_student.name = student.name
        existing_student.age = student.age
        existing_student.course = student.course
        db.commit()
        db.refresh(existing_student)
        return existing_student

    def delete_student_by_id(self, db: Session, student_id: int) -> None:
        existing_student = self.get_student_by_id(db, student_id)
        db.delete(existing_student)
        db.commit()


student_service = StudentService()
        