from database import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class StudentDB(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    course: Mapped[int] = mapped_column(Integer)