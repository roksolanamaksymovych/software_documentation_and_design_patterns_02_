from pydantic import BaseModel
from typing import List, Optional

class ApartmentSchema(BaseModel):
    id: int
    address: str
    price_per_night: float
    is_available: bool
    owner_id: int

    class Config:
        from_attributes = True

class MessageSchema(BaseModel):
    status: str
    count: Optional[int] = None