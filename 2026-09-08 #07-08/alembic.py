from sqlalchemy import create_engine, select, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column

# pip install alembic
# alembic создает и управляет миграциями (версиями) базы данных
# alembic init название_папки (alembic init alembic)
# В alembic.ini нужно прописать путь к базе данных
# sqlalchemy.url = путь к бд
# В env.py импортируем Base и модели
# В env.py ищем target_metadata
# Для создания миграции alembic revision --autogenerate -m "Сообщение"
# alembic upgrade head
# alembic downgrade -1
# alembic downgrade base (откатить все)

engine = create_engine("sqlite:///./database.db") # Движок
SessionLocal = sessionmaker(bind=engine) # Класс сессии 
Base = declarative_base() # Класс базового объекта в базе данных

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    # completed: Mapped[bool] = mapped_column(Boolean, default=False)
    course: Mapped[int] = mapped_column(Integer)
    email: Mapped[str | None] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f"Student(id={self.id}, name={self.name}, age={self.age}, course={self.course})"

# Base.metadata.create_all(engine)

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
    students = session.scalars(select(Student)).all()
    session.close()
    return students

def get_student_by_id(student_id: int):
    session = SessionLocal()
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
#delete_student_by_id(1)
#print(get_all_students())