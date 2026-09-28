from pydantic import BaseModel, Field
from datetime import datetime

class StudentsInCourse(BaseModel):
    id: int
    name: str
    last_name: str
    email: str

class CourseCreate(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    duration: int = Field(gt=0)

class CourseResponse(BaseModel):
    id: int
    name: str
    duration: int
    students: list[StudentsInCourse]

class CourseUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=255)
    duration: int | None = Field(default=None, gt=0)

class CourseEnrolledStudent(StudentsInCourse):
    joined_at: datetime
