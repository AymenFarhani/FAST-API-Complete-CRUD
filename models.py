import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from database import Base


class Project(Base):
    __tablename__ = "projects"
    id :Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    title:Mapped[int] =  mapped_column(String(100), index=True, nullable=False)
    description:Mapped[int] =  mapped_column(String(1000), nullable=True)
    start_date:Mapped[int] =  mapped_column(String(100), default=datetime.date.today())
    status:Mapped[int] =  mapped_column(String, default="In_progress")