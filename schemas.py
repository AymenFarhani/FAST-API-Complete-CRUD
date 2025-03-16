from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    status: Optional[str] = 'In_progress'

class ProjectCreate(ProjectBase):
    pass

    class Config:
        orm_mode = True

class ProjectUpdate(ProjectBase):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True

class ProjectResponse(ProjectBase):
    id: int

    class Config:
        from_attributes= True