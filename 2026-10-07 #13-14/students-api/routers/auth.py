from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db
from dependencies import get_current_user
from models.users import UserDB
from schemas.users import Token, UserCreate, UserResponse
from services.auth_service import auth_service
from sqlalchemy.ext.asyncio import AsyncSession


# pip freeze > requirements.txt
# pip install -r requirements.txt

# Установить Docker проще всего, скачав Docker Desktop
# Docker адекватно на windows не ставится
# Если при запуске видите Virtualization support not detected
# то, вероятнее всего, лечится wsl --install в PowerShell
# После этого нужно запустить Ubuntu

# Пользователь заходит на /auth/login
# Вводит username, password
# Сервер проверяет и возвращает access_token
# Если пользователь заходит на защищенный адрес
# То с клиента приходит токен
# Сервер токен проверяет, идентифицирует пользователя
# И возвращает пользователю запрашиваемые данные
# или 401, если не идентифицирован пользователь

router = APIRouter(prefix="/auth", tags=["auth"])
        

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserDB = Depends(get_current_user)) -> UserResponse:
    return current_user

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, 
                   db: AsyncSession = Depends(get_db)
                ) -> UserResponse:
    return await auth_service.register(db, 
                                 user.username, 
                                 user.password
                            )

@router.post("/login", response_model=Token)
async def login(user: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), 
                db: AsyncSession = Depends(get_db)
            ) -> Token:
    user = await auth_service.authenticate(db, 
                                           user.username, 
                                           user.password
                                        )
    access_token = auth_service.create_access_token(user)
    return Token(access_token=access_token,
                 token_type="Bearer")