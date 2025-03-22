from datetime import timedelta
from typing import List, Annotated

from fastapi import Depends, APIRouter, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette import status
from starlette.responses import StreamingResponse

import database
import export_service
import project_service
import schemas
from auth import CreateUserRequest, bcrypt_context, Token, authenticate_user, create_access_token, get_current_user
from models import User

router = APIRouter()

templates = Jinja2Templates(directory="templates")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict, Depends(get_current_user)]
@router.get('/home', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})

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

@router.get('/export')
def export_projects(db: Session = Depends(database.get_db)):
    excel_file = export_service.export_projects_to_excel(db)
    return StreamingResponse(excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=projects.xlsx"})

@router.post('/user', status_code= status.HTTP_201_CREATED)
async def create_user(db: database.db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(username=create_user_request.username,
                             hashed_password=bcrypt_context.hash(create_user_request.password)
                             )

    db.add(create_user_model)
    db.commit()

@router.post('/auth/token', response_model = Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:database.db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not valid user.")
    token = create_access_token(user.username, user.id, timedelta(minutes=30))
    return {"access_token": token, 'token_type': 'bearer'}

@router.get('/user', status_code= status.HTTP_200_OK)
async def get_user(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail="Authentication Failed!")
    return {"User": user}