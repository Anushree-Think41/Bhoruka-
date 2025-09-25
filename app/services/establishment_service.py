from sqlalchemy.orm import Session
from app.models.establishment_model import Establishment as DBEstablishment
from app.schemas.establishment_schema import EstablishmentCreate, Establishment
from typing import List

def create_establishment(db: Session, establishment: EstablishmentCreate, owner_id: int):
    db_establishment = DBEstablishment(**establishment.model_dump(), owner_id=owner_id)
    db.add(db_establishment)
    db.commit()
    db.refresh(db_establishment)
    return db_establishment

def get_establishment(db: Session, establishment_id: int):
    return db.query(DBEstablishment).filter(DBEstablishment.id == establishment_id).first()

def get_establishments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBEstablishment).offset(skip).limit(limit).all()

def get_establishments_by_owner(db: Session, owner_id: int):
    return db.query(DBEstablishment).filter(DBEstablishment.owner_id == owner_id).all()

def update_establishment(db: Session, establishment_id: int, establishment: EstablishmentCreate):
    db_establishment = db.query(DBEstablishment).filter(DBEstablishment.id == establishment_id).first()
    if db_establishment:
        for key, value in establishment.model_dump().items():
            setattr(db_establishment, key, value)
        db.commit()
        db.refresh(db_establishment)
    return db_establishment

def delete_establishment(db: Session, establishment_id: int):
    db_establishment = db.query(DBEstablishment).filter(DBEstablishment.id == establishment_id).first()
    if db_establishment:
        db.delete(db_establishment)
        db.commit()
    return db_establishment