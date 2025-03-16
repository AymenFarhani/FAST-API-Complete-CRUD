from fastapi import FastAPI
from starlette.templating import Jinja2Templates

import models
from apis import router
from database import engine

project_api = FastAPI(title="Project Management API", version="1.0.0")

templates = Jinja2Templates(directory="templates")


models.Base.metadata.create_all(bind=engine)

project_api.include_router(router, prefix="/api", tags=["Projects"])