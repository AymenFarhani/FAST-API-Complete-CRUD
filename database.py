import os
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
URL_DATABASE = f'postgresql://{username}:{password}@localhost:5432/projects_db'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency =Annotated[Session, Depends(get_db)]