from pydantic import BaseModel, EmailStr
import datetime

class OwnerBase(BaseModel):
    owner_name: str
    primary_phone: str
    secondary_phone: str | None = None
    email: EmailStr | None = None

class OwnerCreate(OwnerBase):
    pass

class Owner(OwnerBase):
    id: int
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None

    class Config:
        from_attributes = True
