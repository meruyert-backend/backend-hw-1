from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from dependencies import get_current_user

from schemas.client import ClientCreate, ClientResponse
from repositories import client_repo

router = APIRouter(prefix="/clients", tags=["Clients"])

#CREATE

@router.post("/", response_model=ClientResponse)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return client_repo.create_client(
        db,
        name=client.name,
        company=client.company,
        notes=client.notes,
        user_id=current_user.id
    )

#GET ALL
@router.get("/", response_model=list[ClientResponse])
def get_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return client_repo.get_clients(db, current_user.id)

#GET ONE
@router.get("/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = client_repo.get_client(db, client_id, current_user.id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client

#UPDATE
@router.put("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    data: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = client_repo.get_client(db, client_id, current_user.id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client_repo.update_client(
        db,
        client,
        name=data.name,
        company=data.company,
        notes=data.notes
    )

#DELETE
@router.delete("/{client_id}")
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = client_repo.get_client(db, client_id, current_user.id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    client_repo.delete_client(db, client)

    return {"message": "Client deleted"}