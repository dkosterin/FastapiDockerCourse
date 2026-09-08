from pydantic import BaseModel, ConfigDict

class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    age: int 
    course: int

class StudentCreate(BaseModel):
    name: str
    age: int 
    course: int