# payload 
#  {
#   "sub": "1234567890", -- идентификатор пользователя (обязательно)
#   Пользовательские поля
#   "name": "Viktor",
#   "role": "user",
#   "iat": 1516239022, -- время создания токена (в секундах от 1 января 1970)
#   "exp": 1516239122, -- время, когда токен перестанет быть актуальным
#                           (в секундах) 
#   "iss": "backend" -- тот, кто выдал токен (идентификатор того, кто выдал)
# }
# header
# {
#   "alg": "HS256",
#   "typ": "JWT"
# }
# signature (подпись сервера) -> signature_code

# Это все кодируется: header -> header_code, payload -> payload_code
# JWT: header_code.payload_code.signature_code

# Для работы с jwt нужно (pip install pyjwt)
# python-jose (устарело, legacy code)
import jwt
import os
# pip install python-dotenv
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Хранят в переменных окружения или файле .env (по сути то же самое, но в рамках одной сессии)
# SECRET_KEY = "secret-string"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 20

def generate_token(data: dict) -> str:
    payload = data.copy()
    payload["iat"] = datetime.now(timezone.utc)
    payload["exp"] = (datetime.now(timezone.utc) + 
                        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# payload
data = {"sub": 123,
        "name": "Viktor", 
        "role": "user"
        }
print(generate_token(data))