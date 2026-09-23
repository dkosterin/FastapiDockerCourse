from models.users import UserDB
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash
from datetime import datetime, timezone, timedelta
import jwt

class UserAlreadyExistException(Exception):
    pass

class AuthException(Exception):
    pass

#Для хеширования паролей библиотека pwdlib
# pip install pwdlib[argon2]

SECRET_KEY = "secret-string"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
    def __init__(self):
        self.password_hash = PasswordHash.recommended()

    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self, 
                        password: str, 
                        password_hash: str
                    ) -> bool:
        return self.password_hash.verify(password, password_hash)

    async def register(self, 
                       db: AsyncSession, 
                       username: str, 
                       password: str
                    ) -> UserDB:
        stmt = select(UserDB).where(UserDB.username == username)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        if existing_user is not None:
            raise UserAlreadyExistException("Пользователь с таким именем уже существует")
        user = UserDB(username=username, 
                      password_hash=self.hash_password(password)
                    )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    async def authenticate(self,
                           db: AsyncSession,
                           username: str,
                           password: str
                        ) ->UserDB:
        stmt = select(UserDB).where(UserDB.username == username)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            raise AuthException("Неверный логин")

        if not self.verify_password(password, user.password_hash):
            raise AuthException("Неверный пароль")
        return user

    def create_access_token(self, user: UserDB) -> str:
        payload = {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role,
            "exp": (datetime.now(timezone.utc) + 
                timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

auth_service = AuthService()