from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from app.database.db_handler import Base
import datetime

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    owner_name = Column(String(255), nullable=False)
    primary_phone = Column(String(20), nullable=False, unique=True)
    secondary_phone = Column(String(20))
    email = Column(String(50), unique=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.datetime.utcnow)

