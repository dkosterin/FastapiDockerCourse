from pydantic import Field, BaseModel, ConfigDict

class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    age: int 
    course: int

class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=16, le=100)
    course: int = Field(ge=1, le=6)