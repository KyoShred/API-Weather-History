from fastapi import Depends, FastAPI, HTTPException

import app.data.models as models
from app.data.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
