from schemas.students import StudentResponse, StudentCreate

class StudentNotFoundException(Exception):
    pass

class StudentService:
    def __init__(self):
        self._students = []


    def get_all_students(self, course: int | None = None) -> list[StudentResponse]:
        if course:
            return [s for s in self._students if s.course == course]
        return self._students


    def get_student_by_id(self, student_id: int) -> StudentResponse:
        for s in self._students:
            if s.id == student_id:
                return s
    
        raise StudentNotFoundException("Студента с таким id нет")


    def append_student(self, student: StudentCreate) -> StudentResponse:
        id = max(s.id for s in self._students) + 1 if len(self._students) > 0 else 1
        s = StudentResponse(id=id, name=student.name, 
                    age=student.age, course=student.course)
        self._students.append(s)
        return s


    def update_student_by_id(self, 
                             student_id: int, 
                             student: StudentCreate) -> StudentResponse:
        for i, s in enumerate(self._students):
            if s.id == student_id:
                self._students[i] = StudentResponse(id=student_id, name=student.name, 
                    age=student.age, course=student.course)
                return self._students[i]
    
        raise StudentNotFoundException("Студента с таким id нет")

    def delete_student_by_id(self, student_id: int) -> None:
        for i in range(len(self._students)):
            if self._students[i].id == student_id:
                del self._students[i]
                return
            
        raise StudentNotFoundException("Студента с таким id нет")


student_service = StudentService()
        