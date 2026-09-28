from fastapi import FastAPI
from app.routers import courses, students, users

app = FastAPI(
    title="Students & Courses API",
    version="0.1.0",
    description="A simple API for managing students and courses",
)

app.include_router(users.router)
app.include_router(courses.router)
app.include_router(students.router)
