import json

from sqlalchemy.orm import Session

import models
import schemas
from schemas import ProjectUpdate


def create_project(db: Session, project: schemas.ProjectCreate):
    new_project = models.Project(**project.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def get_project(project_id: int, db: Session):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Project).offset(skip).limit(limit).all()

def update_project( project_id: int, db: Session, project_data: schemas.ProjectUpdate):
    project = get_project(project_id, db)
    project_data_json = json.loads(project_data)
    project_update = ProjectUpdate.model_validate(project_data_json)
    if not project:
        return None
    for key, value in project_update.model_dump(exclude_unset= True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

def delete_project(project_id: int, db: Session):
    project = get_project(project_id, db)
    if project:
        db.delete(project)
        db.commit()
        return project
    return None