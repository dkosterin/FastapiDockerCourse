from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from services.student_service import student_service
from schemas.students import StudentCreate

pages_router = APIRouter(prefix="/pages", tags=["pages"])
templates = Jinja2Templates(directory="templates")

@pages_router.get("/students", response_class=HTMLResponse)
def get_students_page(request: Request):
    students = student_service.get_all_students()
    return templates.TemplateResponse(request=request,
                                      name="create-student.html",
                                      context={"students": students})


@pages_router.post("/create-student")
def create_student_from_form(request: Request,
                             name: str = Form(...), # ellipsis
                             age: int = Form(...), 
                             course: int = Form(...)):
    student = StudentCreate(name=name, age=age, course=course)
    student_service.append_student(student)
    return RedirectResponse(request.url_for("get_students_page"), status_code=303)