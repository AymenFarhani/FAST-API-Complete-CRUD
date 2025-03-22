import datetime

from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import mapped_column, Mapped

from database import Base


class Project(Base):
    __tablename__ = "projects"
    id :Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    title:Mapped[str] =  mapped_column(String(100), index=True, nullable=False)
    description:Mapped[str] =  mapped_column(String(1000), nullable=True)
    start_date:Mapped[str] =  mapped_column(String(100), default=datetime.date.today())
    status:Mapped[str] =  mapped_column(String, default="In_progress")


class User(Base):
    __tablename__ = "users"


    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    username:Mapped[str] =  mapped_column(String, unique=True)
    hashed_password:Mapped[str] = mapped_column(String)