from sqlalchemy.orm import Session
from app.models.owner_model import Owner as DBOwner
from app.schemas.owner_schema import OwnerCreate, Owner

def create_owner(db: Session, owner: OwnerCreate):
    db_owner = DBOwner(**owner.model_dump())
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner

def get_owner(db: Session, owner_id: int):
    return db.query(DBOwner).filter(DBOwner.id == owner_id).first()

def get_owner_by_email(db: Session, email: str):
    return db.query(DBOwner).filter(DBOwner.email == email).first()

def get_owner_by_phone(db: Session, phone: str):
    return db.query(DBOwner).filter(DBOwner.primary_phone == phone).first()

def get_owners(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBOwner).offset(skip).limit(limit).all()

def update_owner(db: Session, owner_id: int, owner: OwnerCreate):
    db_owner = db.query(DBOwner).filter(DBOwner.id == owner_id).first()
    if db_owner:
        for key, value in owner.model_dump().items():
            setattr(db_owner, key, value)
        db.commit()
        db.refresh(db_owner)
    return db_owner

def delete_owner(db: Session, owner_id: int):
    db_owner = db.query(DBOwner).filter(DBOwner.id == owner_id).first()
    if db_owner:
        db.delete(db_owner)
        db.commit()
    return db_owner
