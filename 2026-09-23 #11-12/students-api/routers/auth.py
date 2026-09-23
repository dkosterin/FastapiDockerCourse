from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.users import Token, UserCreate, UserResponse
from services.auth_service import auth_service
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])

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