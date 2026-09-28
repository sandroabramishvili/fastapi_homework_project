from fastapi import APIRouter, Depends, HTTPException, status
from app.models.courses import Course
from app.models.associations import StudentCourse
from app.models.students import Student
from app.schemas.courses import CourseCreate, CourseResponse, CourseUpdate, CourseEnrolledStudent
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("/", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):

    existing_course = db.query(Course).filter(Course.name == course.name).first()

    if existing_course:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course already exists with this name")

    new_course = Course(name=course.name, duration=course.duration)

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    return course

@router.patch("/{course_id}", response_model=CourseResponse, status_code=status.HTTP_200_OK)
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    course_to_update = db.query(Course).filter(Course.id == course_id).first()

    if not course_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    update_data = course.model_dump(exclude_unset=True)

    if "name" in update_data:
        existing_course = db.query(Course).filter(Course.name == update_data["name"]).first()

        if existing_course and existing_course.id != course_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course already exists with this name")

    for field, value in update_data.items():
        setattr(course_to_update, field, value)

    db.commit()
    db.refresh(course_to_update)

    return course_to_update


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course_to_delete = db.query(Course).filter(Course.id == course_id).first()

    if not course_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    db.delete(course_to_delete)
    db.commit()


@router.get("/{course_id}/students", response_model=list[CourseEnrolledStudent])
def get_course_students(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    rows = (
        db.query(Student, StudentCourse.joined_at)
        .join(StudentCourse, StudentCourse.student_id == Student.id)
        .filter(StudentCourse.course_id == course_id)
        .all()
    )

    return [
        {"id": s.id, "name": s.name, "last_name": s.last_name, "email": s.email, "joined_at": joined_at}
        for s, joined_at in rows
    ]
