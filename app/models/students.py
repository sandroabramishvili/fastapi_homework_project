from app.database import Base
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    courses: Mapped[list["Course"]] = relationship(secondary="student_courses", viewonly=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"
