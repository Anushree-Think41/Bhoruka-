from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import datetime

from app.database.db_handler import get_db
from app.models.owner_model import Owner as DBOwner
from app.models.establishment_model import Establishment as DBEstablishment
from app.schemas.owner_schema import Owner, OwnerCreate
from app.schemas.establishment_schema import Establishment
import app.services.owner_service as owner_service
import app.services.establishment_service as establishment_service

router = APIRouter(
    prefix="/owners",
    tags=["owners"]
)

@router.post("/", response_model=Owner, status_code=status.HTTP_201_CREATED)
def create_owner(owner: OwnerCreate, db: Session = Depends(get_db)):
    db_owner = owner_service.get_owner_by_email(db, email=owner.email)
    if db_owner:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    return owner_service.create_owner(db=db, owner=owner)

@router.get("/", response_model=List[Owner])
def read_owners(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    owners = owner_service.get_owners(db, skip=skip, limit=limit)
    return owners

@router.get("/{owner_id}", response_model=Owner)
def read_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = owner_service.get_owner(db, owner_id=owner_id)
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")
    return owner

@router.get("/{owner_id}/establishments", response_model=List[Establishment])
def read_establishments_for_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = owner_service.get_owner(db, owner_id=owner_id)
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")
    establishments = establishment_service.get_establishments_by_owner(db, owner_id=owner_id)
    if not establishments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No establishments found for this owner")
    return establishments

@router.put("/{owner_id}", response_model=Owner)
def update_owner(owner_id: int, owner: OwnerCreate, db: Session = Depends(get_db)):
    db_owner = owner_service.update_owner(db, owner_id=owner_id, owner=owner)
    if db_owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")
    return db_owner

@router.delete("/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_owner(owner_id: int, db: Session = Depends(get_db)):
    db_owner = owner_service.delete_owner(db, owner_id=owner_id)
    if db_owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")
    return