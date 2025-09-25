from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List
import datetime

from app.database.db_handler import get_db
from app.models.establishment_model import Establishment as DBEstablishment
from app.schemas.establishment_schema import Establishment, EstablishmentCreate

router = APIRouter(
    prefix="/establishments",
    tags=["establishments"]
)

@router.post("/", response_model=Establishment, status_code=status.HTTP_201_CREATED)
def create_establishment(establishment: EstablishmentCreate, owner_id: int = Header(...), db: Session = Depends(get_db)):
    db_establishment = DBEstablishment(
        owner_id=owner_id,
        establishment_name=establishment.establishment_name,
        address=establishment.address,
        city=establishment.city,
        state=establishment.state,
        pincode=establishment.pincode,
        gstin=establishment.gstin,
        offerings=establishment.offerings
    )
    db.add(db_establishment)
    db.commit()
    db.refresh(db_establishment)
    return db_establishment

@router.get("/", response_model=List[Establishment])
def read_establishments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    establishments = db.query(DBEstablishment).offset(skip).limit(limit).all()
    return establishments

@router.get("/{establishment_id}", response_model=Establishment)
def read_establishment(establishment_id: int, db: Session = Depends(get_db)):
    establishment = db.query(DBEstablishment).filter(DBEstablishment.id == establishment_id).first()
    if establishment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Establishment not found")
    return establishment

@router.put("/{establishment_id}", response_model=Establishment)
def update_establishment(establishment_id: int, establishment: EstablishmentCreate, db: Session = Depends(get_db)):
    db_establishment = db.query(DBEstablishment).filter(DBEstablishment.id == establishment_id).first()
    if db_establishment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Establishment not found")
    
    db_establishment.establishment_name = establishment.establishment_name
    db_establishment.address = establishment.address
    db_establishment.city = establishment.city
    db_establishment.state = establishment.state
    db_establishment.pincode = establishment.pincode
    db_establishment.gstin = establishment.gstin
    db_establishment.offerings = establishment.offerings

    db.commit()
    db.refresh(db_establishment)
    return db_establishment

@router.delete("/{establishment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_establishment(establishment_id: int, db: Session = Depends(get_db)):
    db_establishment = db.query(DBEstablishment).filter(DBEstablishment.id == establishment_id).first()
    if db_establishment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Establishment not found")
    
    db.delete(db_establishment)
    db.commit()
    return 