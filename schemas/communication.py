from pydantic import BaseModel

#CREATE
class CommunicationCreate(BaseModel):
    text: str
    client_id: int

#CREATE
class CommunicationResponse(BaseModel):
    id: int
    text: str
    client_id: int

    class Config:
        from_attributes = True


#RESPONSE
class CommunicationResponse(BaseModel):
    id: int
    text: str
    client_id: int

    class Config:
        from_attributes = True

