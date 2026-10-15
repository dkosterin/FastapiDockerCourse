
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.users import UserDB
from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#OAuth2PasswordBearer это зависимость, которая извлекает токен
# из заголовка 

async def get_current_user(token: str = Depends(oauth2_scheme), 
                           db: AsyncSession = Depends(get_db)
                           ):
   try:
      #JWT: header.payload.signature
      payload = jwt.decode(token, 
                           settings.secret_key,
                           algorithms=[settings.algorithm])
      user_id = payload.get("sub")
      if user_id is None:
          raise HTTPException(status_code=401, 
                            detail="Не можем определить пользователя")
      stmt = select(UserDB).where(UserDB.id == int(user_id))
      result = await db.execute(stmt)
      user = result.scalar_one_or_none()
      if user is not None:
          return user
      else:
          raise HTTPException(status_code=401, 
                                  detail="Не можем определить пользователя")
   except jwt.InvalidTokenError:
      raise HTTPException(status_code=401, 
                        detail="Не можем определить пользователя")

async def require_admin(current_user: UserDB = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, 
                                     detail="Недостаточно прав")
    return current_user

async def get_redis(request: Request):
    return request.app.state.redis