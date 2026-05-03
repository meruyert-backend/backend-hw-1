from pydantic import BaseModel
from typing import Optional

class ClientCreate(BaseModel):
    name: str
    company: Optional[str] = None
    notes: Optional[str] = None

class ClientResponse(BaseModel):
    id: int
    name: str
    company: Optional[str]
    notes: Optional[str]

    class Config:
        from_attributes = True

