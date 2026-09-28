from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    duration: Mapped[int] = mapped_column(Integer)
    students: Mapped[list["Student"]] = relationship(secondary="student_courses", viewonly=True)

    def __str__(self):
        return self.name
