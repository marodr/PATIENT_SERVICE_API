#!/usr/bin/env python
""" This is the entrypoint to the Patient Service API.
"""

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from lib import appointment_crud, employee_crud, hospital_crud, patient_crud, physician_crud, department_crud, prescription_crud, medication_crud, insurance_crud
from lib import response_models
from lib.database_connection import SessionLocal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = patient_crud.get_patients(db, skip=skip, limit=limit)
    return patients

@app.get("/patients/{id}", response_model=response_models.Patient, tags=["Patient Methods"])
def get_patients_by_id(id:int , db: Session = Depends(get_db)):
    patient = patient_crud.get_patient(db, id)
    return patient

@app.delete("/patients/{id}", tags=["Patient Methods"])
def delete_patient_by_id(id: int, db:Session = Depends(get_db)):
    patient = patient_crud.delete_patient(db, id)
    return patient



@app.get("/physicians/", response_model=List[response_models.Physician])
def get_physicians(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    physicians = physician_crud.get_physicians(db, skip=skip, limit=limit)
    return physicians

@app.get("/departments/", response_model=List[response_models.Department])
def get_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departments = department_crud.get_departments(db, skip=skip, limit=limit)
    return departments

@app.get("/prescriptions/", response_model=List[response_models.Prescription])
def get_prescriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prescriptions = prescription_crud.get_prescriptions(db, skip=skip, limit=limit)
    return prescriptions

@app.get("/medications/", response_model=List[response_models.Medication])
def get_medications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    medications = medication_crud.get_medications(db, skip=skip, limit=limit)
    return medications

@app.get("/insurances/", response_model=List[response_models.Insurance])
def get_insurance(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    insurances = insurance_crud.get_insurance(db, skip=skip, limit=limit)
    return insurances

@app.get("/employees/", response_model=List[response_models.Employee])
def get_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = employee_crud.get_employees(db, skip=skip, limit=limit)
    return employees

@app.get("/hospitals/", response_model=List[response_models.Hospital])
def get_hospitals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    hospitals = hospital_crud.get_hospitals(db, skip=skip, limit=limit)
    return hospitals

@app.get("/appointments/", response_model=List[response_models.Appointment])
def get_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = appointment_crud.get_appointments(db, skip=skip, limit=limit)
    return appointments