from pydantic import BaseModel
from datetime import datetime

class CoursesForStudent(BaseModel):
    id: int
    name: str
    duration: int

class StudentCreate(BaseModel):
    name: str
    last_name: str
    email: str

class StudentResponse(BaseModel):
    id: int
    name: str
    last_name: str
    email: str
    courses: list[CoursesForStudent]

class StudentUpdate(BaseModel):
    name: str | None = None
    last_name: str | None = None
    email: str | None = None

class StudentCourseResponse(BaseModel):
    student_id: int
    course_id: int
    joined_at: datetime

class StudentEnrolledCourse(CoursesForStudent):
    joined_at: datetime
