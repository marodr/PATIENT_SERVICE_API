# -*- coding: utf-8 -*-
from fastapi import HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from . import db_models


def get_patient(db: Session, patient_id: int):
    return db.query(db_models.Patient).filter(db_models.Patient.id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Patient).offset(skip).limit(limit).all()

def create_patient(db:Session, patient):
    #Find physicians with least number of patients
    subquery = (
        db.query(db_models.Physician.id, func.count(db_models.Patient.id).label("patient_count"))
        .outerjoin(db_models.Patient, db_models.Physician.id == db_models.Patient.physician_id)
        .groupby(db_models.Physicians.id)
        .subquery()
    )
    least_busy_physician = db.query(subquery.c.id).order_by(subquery.c.patient_count.asc()).first()

    if not least_busy_physician:
        raise HTTPException(status_code=404, detail="No physician available")
    #create the patient with the physician id of the least busy physician
    patient_data = patient.dict()
    patient_data["physician_id"] = least_busy_physician.id
    db_patient = db_models.Patient(**patient_data)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


# Delete - Remove a patient
def delete_patient(db: Session, patient_id: int):
    # first, check if patient exists
    db_patient = db.query(db_models.Patient).filter(db_models.Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    #Explicitly delete dependencies
    #Delete all related appointments
    db.query(db_models.Appointment).filter(db_models.Appointment.patient_id == patient_id).delete()
    #Delete all related prescriptions
    db.query(db_models.Prescription).filter(
        db_models.Prescription.patient_id == patient_id
    ).delete()
    #Delete all related insurance records
    db.query(db_models.Insurance).filter(db_models.Insurance.patient_id == patient_id).delete()

    #finally delete the patient
    db.delete(db_patient)
    db.commit()
    return {"ok": True}