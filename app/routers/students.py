from fastapi import APIRouter, Depends, HTTPException, status
from app.models.students import Student
from app.models.courses import Course
from app.models.associations import StudentCourse
from app.schemas.students import StudentCreate, StudentResponse, StudentUpdate, StudentCourseResponse, StudentEnrolledCourse
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):

    existing_student = db.query(Student).filter(Student.email == student.email).first()

    if existing_student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already exists with this email")

    new_student = Student(**student.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    return student

@router.patch("/{student_id}", response_model=StudentResponse, status_code=status.HTTP_200_OK)
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    student_to_update = db.query(Student).filter(Student.id == student_id).first()

    if not student_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    update_data = student.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing_student = db.query(Student).filter(Student.email == update_data["email"]).first()

        if existing_student and existing_student.id != student_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already exists with this email")

    for field, value in update_data.items():
        setattr(student_to_update, field, value)

    db.commit()
    db.refresh(student_to_update)

    return student_to_update


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student_to_delete = db.query(Student).filter(Student.id == student_id).first()

    if not student_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    db.delete(student_to_delete)
    db.commit()


@router.post("/{student_id}/courses/{course_id}", response_model=StudentCourseResponse, status_code=status.HTTP_201_CREATED)
def enroll_student(student_id: int, course_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    if db.get(StudentCourse, (student_id, course_id)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student is already enrolled in this course")

    enrollment = StudentCourse(student_id=student_id, course_id=course_id)

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment


@router.get("/{student_id}/courses", response_model=list[StudentEnrolledCourse])
def get_student_courses(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    rows = (
        db.query(Course, StudentCourse.joined_at)
        .join(StudentCourse, StudentCourse.course_id == Course.id)
        .filter(StudentCourse.student_id == student_id)
        .all()
    )

    return [
        {"id": c.id, "name": c.name, "duration": c.duration, "joined_at": joined_at}
        for c, joined_at in rows
    ]


@router.delete("/{student_id}/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def unenroll_student(student_id: int, course_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    enrollment = db.get(StudentCourse, (student_id, course_id))

    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student is not enrolled in this course")

    db.delete(enrollment)
    db.commit()
