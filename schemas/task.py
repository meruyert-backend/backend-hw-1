from pydantic import BaseModel
from typing import Optional

#CREATE
class TaskCreate(BaseModel):
    title: str
    deadline: Optional[str] = None
    client_id: int


#UPDATE
class TaskUpdate(BaseModel):
    title: str
    deadline: Optional[str] = None
    status: str


#RESPONSE
class TaskResponse(BaseModel):
    id: int
    title: str
    deadline: Optional[str]
    status: str
    client_id: int

    class Config:
        from_attributes = True


