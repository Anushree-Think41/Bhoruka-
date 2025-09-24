from sqlalchemy import Column, Integer, String, DateTime
from app.database.db_handler import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    last_login = Column(DateTime, default=datetime.datetime.utcnow)