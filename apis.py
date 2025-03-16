
from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
import database
import project_service
import schemas

router = APIRouter()

@router.post('/project', response_model=schemas.ProjectResponse)
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(database.get_db)):
    return project_service.create_project(db, project)

@router.get('/projects', response_model=List[schemas.ProjectResponse])
async def get_projects(db: Session = Depends(database.get_db)):
    return project_service.get_projects(db)

@router.get('/project/{id}', response_model=schemas.ProjectResponse)
async def get_project(id: int, db: Session = Depends(database.get_db)):
    project = project_service.get_project(id, db)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put('/project/{id}', response_model=schemas.ProjectResponse)
async def update_project(id: int, db: Session = Depends(database.get_db), updated_project= schemas.ProjectUpdate):
    project = project_service.update_project(id, db, updated_project)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete('/project/{id}')
async def delete_project(id: int, db: Session = Depends(database.get_db)):
    project = project_service.get_project(id, db)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    project_service.delete_project(id, db)
    return {"message": "Project deleted successfully"}