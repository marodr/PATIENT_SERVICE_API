from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from . import db_models


def get_patient(db: Session, patient_id: int):
    return db.query(db_models.Patient).filter(db_models.Patient.id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 100, sort="desc"):
    if sort not in ['desc','asc']:
        raise Exception("Sort should be either desc or asc")
    if sort == "asc":
        return db.query(db_models.Patient).order_by(asc(db_models.Patient.id)).offset(skip).limit(limit).all()
    return db.query(db_models.Patient).order_by(desc(db_models.Patient.id)).offset(skip).limit(limit).all()

