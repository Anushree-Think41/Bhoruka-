from pydantic import BaseModel
import datetime
from typing import List

class EstablishmentBase(BaseModel):
    establishment_name: str
    address: str
    city: str | None = None
    state: str | None = None
    pincode: str
    gstin: str | None = None
    offerings: List[str]

class EstablishmentCreate(EstablishmentBase):
    pass
class Establishment(EstablishmentBase):
    id: int
    owner_id: int
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None

    class Config:
        from_attributes = True
