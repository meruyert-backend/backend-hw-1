from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models.user import User

from schemas.communication import CommunicationCreate, CommunicationResponse
from repositories import communication_repo, client_repo

from services.ai_service import extract_tasks
from repositories import task_repo

router = APIRouter(prefix="/communications", tags=["Communications"])

#CREATE
@router.post("/", response_model=CommunicationResponse)
def create_communication(
    data: CommunicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = client_repo.get_client(db, data.client_id, current_user.id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    comm = communication_repo.create_communication(
        db,
        text=data.text,
        client_id=data.client_id
    )

    # AI part
    # AI part
    try:
        tasks = extract_tasks(data.text)
        print("AI TASKS:", tasks)

        if tasks:
            for t in tasks:
                task_repo.create_task(
                    db,
                    title=t.get("title"),
                    deadline=t.get("deadline"),
                    client_id=data.client_id,
                    communication_id=comm.id
                )

    except Exception as e:
        print("AI ERROR:", e)

    return comm


#GET ALL
@router.get("/", response_model=list[CommunicationResponse])
def get_communications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return communication_repo.get_communications(db, current_user.id)


#GET ONE
@router.get("/{comm_id}", response_model=CommunicationResponse)
def get_communication(
    comm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comm = communication_repo.get_communication(db, comm_id, current_user.id)

    if not comm:
        raise HTTPException(status_code=404, detail="Communication not found")

    return comm


#DELETE
@router.delete("/{comm_id}")
def delete_communication(
    comm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comm = communication_repo.get_communication(db, comm_id, current_user.id)

    if not comm:
        raise HTTPException(status_code=404, detail="Communication not found")

    communication_repo.delete_communication(db, comm)

    return {"message": "Communication deleted"}
