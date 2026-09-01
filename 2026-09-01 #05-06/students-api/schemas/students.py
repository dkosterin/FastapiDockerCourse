from pydantic import BaseModel

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int 
    course: int

class StudentCreate(BaseModel):
    name: str
    age: int 
    course: int