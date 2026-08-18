from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Виртуальное окружение
# python -m venv venv
# venv\Scripts\activate (Windows)
# source venv/bin/activate (Linux/MacOS)
# deactivate для выхода из виртуального окружения
# Установка библиотек 
# Глобально python -m pip
# pip install fastapi uvicorn
# uvicorn main:app --reload 

#https://github.com/dkosterin/FastapiDockerCourse

# Список студентов (id, name, age, course), 
# GET (получить список студентов), POST (добавление студента), 
# PUT (изменение студента), DELETE (удаление)

# Модель (схема)
class Student(BaseModel):
    id: int
    name: str
    age: int 
    course: int

# {
# id: 1,
# name: "Victor",
# age: "aaaa",
# course: 2
# }

class StudentCreate(BaseModel):
    name: str
    age: int 
    course: int

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", # адрес клиента
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

students = []

@app.get("/students")
def get_students(course: int | None=None) -> list[Student]:
    # result = []
    # for s in students:
    #     if s.course == course:
    #         result.append(s)
    if course:
        return [s for s in students if s.course == course]
    return students

@app.get("/students/{id}")
def get_student_by_id(id: int) -> Student:
    for s in students:
        if s.id == id:
            return s

    raise HTTPException(404, detail="Такого студента нет")

@app.post("/students")
def add_student(student: StudentCreate) -> Student:
    id = max(s.id for s in students) + 1 if len(students) > 0 else 1
    s = Student(id=id, name=student.name, 
                age=student.age, course=student.course)
    students.append(s)
    return s

@app.put("/students/{id}")
def update_student_by_id(id: int, student: StudentCreate) -> Student:
    for i, s in enumerate(students):
        if s.id == id:
            students[i] = Student(id=id, name=student.name, 
                age=student.age, course=student.course)
            return students[i]

    raise HTTPException(404, detail="Такого студента нет")

@app.delete("/students/{id}")
def delete_student(id: int):
    for i in range(len(students)):
        if students[i].id == id:
            del students[i]
            return
    raise HTTPException(404, detail="Такого студента нет")
    