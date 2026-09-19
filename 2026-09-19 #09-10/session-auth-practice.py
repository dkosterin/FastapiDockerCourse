from fastapi import Cookie, FastAPI, Response, HTTPException
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

app = FastAPI()

users = {"user": "12345", "admin": "admin"}
# Ключ - username, значение - пароль
sessions = {}

def is_user_exist(username: str, password: str) -> bool:
    return username in users and users[username] == password

@app.post("/login")
def login(request: LoginRequest, response: Response):
    if not is_user_exist(request.username, request.password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    session_token = request.username
    sessions[request.username] = session_token

    response.set_cookie(key="session_token", value=session_token)

    return {"message": "Authorized"}

@app.get("/protected-page")
def protected_page(session_token: str | None = Cookie(None)):
    if session_token is None or session_token not in sessions:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {"message": "Welcome!"}

@app.post("/logout")
def logout(session_token: str | None = Cookie(None), response: Response = None):
    if session_token is None or session_token not in sessions:
        raise HTTPException(status_code=401, detail="Unauthorized")

    del sessions[session_token]
    response.delete_cookie(key="session_token")

    return {"message": "Logout"}