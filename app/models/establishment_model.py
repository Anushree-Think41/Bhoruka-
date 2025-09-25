from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Text, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db_handler import Base
import datetime

class Establishment(Base):
    __tablename__ = "establishments"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)
    establishment_name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(128))
    state = Column(String(15))
    pincode = Column(String(20), nullable=False)
    gstin = Column(String(15), unique=True)
    offerings = Column(ARRAY(Text), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.datetime.utcnow)

    owner = relationship("Owner")
