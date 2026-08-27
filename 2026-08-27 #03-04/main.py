from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Jinja2 - библиотека для формирования HTML в ответы на запросы
# pip install jinja2

app = FastAPI()
templates = Jinja2Templates(directory="templates") # шаблоны (HTML документы)
# directory - директория, где хранятся шаблоны

@app.get("/hello", response_class=HTMLResponse)
def greetings(request: Request):
    return templates.TemplateResponse(request=request, name="hello.html")

# Объект хэшируемый, если в ее классе переопределен __hash__

@app.get("/hello/{name}", response_class=HTMLResponse)
def greetings_by_name(request: Request, name: str):
    users = ["Alexey", "Andrey", "Ivan"]
    return templates.TemplateResponse(request=request, 
                                      name="greetings.html",
                                      context={"name": name,
                                               "is_admin": True,
                                               "users": users})