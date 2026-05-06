from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models.user import User

from schemas.communication import CommunicationCreate, CommunicationResponse
from repositories import communication_repo, client_repo

from services.ai_service import extract_tasks
from repositories import task_repo


from fastapi import Form
from fastapi.responses import RedirectResponse

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

    return comm



@router.post("/form")
def create_communication_form(
    text: str = Form(...),
    client_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    communication_repo.create_communication(
        db=db,
        text=text,
        client_id=client_id
    )

    return RedirectResponse(url="/communications-page", status_code=303)



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
