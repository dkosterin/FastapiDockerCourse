from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from services.student_service import student_service
from schemas.students import StudentCreate
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db

pages_router = APIRouter(prefix="/pages", tags=["pages"])
templates = Jinja2Templates(directory="templates")

@pages_router.get("/students", response_class=HTMLResponse)
def get_students_page(request: Request, db: Session = Depends(get_db)):
    students = student_service.get_all_students(db)
    return templates.TemplateResponse(request=request,
                                      name="create-student.html",
                                      context={"students": students})


@pages_router.post("/create-student")
def create_student_from_form(request: Request,
                             name: str = Form(...), # ellipsis
                             age: int = Form(...), 
                             course: int = Form(...),
                             db: Session = Depends(get_db)):
    student = StudentCreate(name=name, age=age, course=course)
    student_service.append_student(db, student)
    return RedirectResponse(request.url_for("get_students_page"), status_code=303)