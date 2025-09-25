from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import datetime

from app.database.db_handler import get_db
from app.models.owner_model import Owner as DBOwner
from app.models.establishment_model import Establishment as DBEstablishment
from app.schemas.owner_schema import Owner, OwnerCreate
from app.schemas.establishment_schema import Establishment

router = APIRouter(
    prefix="/owners",
    tags=["owners"]
)

@router.post("/", response_model=Owner, status_code=status.HTTP_201_CREATED)
def create_owner(owner: OwnerCreate, db: Session = Depends(get_db)):
    db_owner = db.query(DBOwner).filter(DBOwner.email == owner.email).first()
    if db_owner:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    db_owner = DBOwner(
        owner_name=owner.owner_name,
        primary_phone=owner.primary_phone,
        secondary_phone=owner.secondary_phone,
        email=owner.email
    )
    db.add(db_owner)
    db.commit()
    db.flush()
    db.refresh(db_owner)
    return db_owner

@router.get("/", response_model=List[Owner])
def read_owners(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    owners = db.query(DBOwner).offset(skip).limit(limit).all()
    return owners

@router.get("/{owner_id}", response_model=Owner)
def read_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(DBOwner).filter(DBOwner.id == owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")
    return owner

@router.get("/{owner_id}/establishments", response_model=List[Establishment])
def read_establishments_for_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(DBOwner).filter(DBOwner.id == owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")
    establishments = db.query(DBEstablishment).filter(DBEstablishment.owner_id == owner_id).all()
    if not establishments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No establishments found for this owner")
    return establishments

@router.put("/{owner_id}", response_model=Owner)
def update_owner(owner_id: int, owner: OwnerCreate, db: Session = Depends(get_db)):
    db_owner = db.query(DBOwner).filter(DBOwner.id == owner_id).first()
    if db_owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")
    
    db_owner.owner_name = owner.owner_name
    db_owner.primary_phone = owner.primary_phone
    db_owner.secondary_phone = owner.secondary_phone
    db_owner.email = owner.email

    db.commit()
    db.refresh(db_owner)
    return db_owner

@router.delete("/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_owner(owner_id: int, db: Session = Depends(get_db)):
    db_owner = db.query(DBOwner).filter(DBOwner.id == owner_id).first()
    if db_owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")
    
    db.delete(db_owner)
    db.commit()
    return 