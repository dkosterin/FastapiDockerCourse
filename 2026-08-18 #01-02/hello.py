from fastapi import FastAPI

# Виртуальное окружение
# python -m venv venv
# venv\Scripts\activate (Windows)
# source venv/bin/activate (Linux/MacOS)
# deactivate для выхода из виртуального окружения
# Установка библиотек 
# Глобально python -m pip
# pip install fastapi uvicorn
# uvicorn main:app --reload 

#https://github.com/dkosterin/FastapiDockerCourse

app = FastAPI()

#QUERY-параметры http://localhost:8000/hello?name=Alexey
@app.get("/hello")
def hello(name: str=""):
    if name != "":
        return {"message": f"Hello, {name}!"}
    return {"message": "Hello!"}

# PATH-параметры
@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello, {name}!"}

@app.post("/number")
def func(number: int):
    return {"Your number": number}