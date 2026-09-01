# sqlite3 -- СУБД, встроенная в python
# sqlalchemy -- библиотека для работы с базами данных
# pip install sqlalchemy
from sqlalchemy import create_engine, select, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column

# ORM object-relative mapping

engine = create_engine("sqlite:///./database.db") # Движок
SessionLocal = sessionmaker(bind=engine) # Класс сессии 
Base = declarative_base() # Класс базового объекта в базе данных

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    course: Mapped[int] = mapped_column(Integer)
    #email: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f"Student(id={self.id}, name={self.name}, age={self.age}, course={self.course})"

Base.metadata.create_all(engine)

def create_student(name: str, age: int, course: int):
    session = SessionLocal()
    student = Student(name=name, age=age, course=course)
    session.add(student)
    session.commit() # Внесение наших изменение в БД
    session.refresh(student)
    session.close()
    return student

def get_all_students():
    session = SessionLocal()
    #stmt = select(Student.name, Student.course)
    #print(stmt)
    # execute не возвращает список объектов класса Student
    # print(session.scalars(stmt).all())
    #print(session.execute(stmt).scalars().all())
    students = session.scalars(select(Student)).all()
    session.close()
    return students

def get_student_by_id(student_id: int):
    session = SessionLocal()
    # stmt = select(Student).where(Student.id == student_id)
    # student = session.scalars(stmt).first()
    student = session.get(Student, student_id)
    session.close()
    return student

def update_student_by_id(student_id: int, name: str, age: int, course: int):
    #with SessionLocal() as session: можно вот так
    session = SessionLocal()
    existing_student = session.get(Student, student_id)
    existing_student.name = name
    existing_student.age = age
    existing_student.course = course
    session.commit()
    session.refresh(existing_student)
    session.close()
    return existing_student

def delete_student_by_id(student_id: int):
    session = SessionLocal()
    existing_student = session.get(Student, student_id)
    session.delete(existing_student)
    session.commit()
    session.close()

# create_student("Sergey", 19, 2)
# print(get_all_students())
# print(get_student_by_id(1))
# print(update_student_by_id(3, "Igor", 19, 1))
# print(get_student_by_id(3))
# delete_student_by_id(2)
print(get_all_students())