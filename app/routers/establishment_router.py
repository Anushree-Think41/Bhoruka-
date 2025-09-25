from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List
import datetime

from app.database.db_handler import get_db
from app.models.establishment_model import Establishment as DBEstablishment
from app.schemas.establishment_schema import Establishment, EstablishmentCreate
import app.services.establishment_service as establishment_service

router = APIRouter(
    prefix="/establishments",
    tags=["establishments"]
)

@router.post("/", response_model=Establishment, status_code=status.HTTP_201_CREATED)
def create_establishment(establishment: EstablishmentCreate, owner_id: int = Header(...), db: Session = Depends(get_db)):
    return establishment_service.create_establishment(db=db, establishment=establishment, owner_id=owner_id)

@router.get("/", response_model=List[Establishment])
def read_establishments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    establishments = establishment_service.get_establishments(db, skip=skip, limit=limit)
    return establishments

@router.get("/{establishment_id}", response_model=Establishment)
def read_establishment(establishment_id: int, db: Session = Depends(get_db)):
    establishment = establishment_service.get_establishment(db, establishment_id=establishment_id)
    if establishment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Establishment not found")
    return establishment

@router.put("/{establishment_id}", response_model=Establishment)
def update_establishment(establishment_id: int, establishment: EstablishmentCreate, db: Session = Depends(get_db)):
    db_establishment = establishment_service.update_establishment(db, establishment_id=establishment_id, establishment=establishment)
    if db_establishment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Establishment not found")
    
    return db_establishment

@router.delete("/{establishment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_establishment(establishment_id: int, db: Session = Depends(get_db)):
    db_establishment = establishment_service.delete_establishment(db, establishment_id=establishment_id)
    if db_establishment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Establishment not found")
    
    return 