#!/usr/bin/env python
""" This is the entrypoint to the Patient Service API.
"""

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session

from lib import patient_crud, physician_crud
from lib import response_models
from lib.database_connection import SessionLocal

app = FastAPI()



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/patients/", response_model=List[response_models.Patient])
def get_patients(skip: int = 0, limit: int = 100, sort="desc", db: Session = Depends(get_db)):
    try:
        patients = patient_crud.get_patients(db, skip=skip, limit=limit, sort=sort)
        return patients
    except:
        raise HTTPException(status_code=418, detail=f"Error getting patients")

@app.get("/physicians/", response_model=List[response_models.Physician])
def get_physicians(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    physicians = physician_crud.get_physicians(db, skip=skip, limit=limit)
    return physicians