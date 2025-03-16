from fastapi import FastAPI

import models
from apis import router
from database import engine

project_api = FastAPI(title="Project Management API", version="1.0.0")

models.Base.metadata.create_all(bind=engine)

project_api.include_router(router, prefix="/api", tags=["Projects"])