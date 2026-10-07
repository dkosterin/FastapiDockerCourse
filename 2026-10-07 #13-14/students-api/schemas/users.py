from pydantic import BaseModel, ConfigDict

# 1. Регистрация пользователя
# 2. Логин
# 3. Защищенные эндпоинты

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    role: str

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str