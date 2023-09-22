from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from data import crud, models, schemas
from data.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
