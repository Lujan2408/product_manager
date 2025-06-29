# Database connection
from sqlmodel import Session, create_engine, SQLModel
from app.core.config import settings  
from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
import app.models as models
from typing import Annotated

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)

def create_db_and_tables():
  SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
  create_db_and_tables()
  yield

def get_session():
  with Session(engine) as session:
    yield session

SessionDependency = Annotated[Session, Depends(get_session)]