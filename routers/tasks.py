from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models.user import User

from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from repositories import task_repo, client_repo

from fastapi import Form
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

#CREATE
@router.post("/", response_model=TaskResponse)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = client_repo.get_client(db, data.client_id, current_user.id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return task_repo.create_task(
        db,
        title=data.title,
        deadline=data.deadline,
        client_id=data.client_id,
        user_id=current_user.id
    )

@router.post("/form")
def create_task_form(
    title: str = Form(...),
    deadline: str = Form(None),
    client_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task_repo.create_task(
        db=db,
        title=title,
        deadline=deadline,
        client_id=client_id
    )

    return RedirectResponse(url="/tasks-page", status_code=303)




#UPDATE
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = task_repo.get_task(db, task_id, current_user.id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_repo.update_task(
        db,
        task,
        title=data.title,
        deadline=data.deadline,
        status=data.status
    )


#DELETE
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = task_repo.get_task(db, task_id, current_user.id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_repo.delete_task(db, task)

    return {"message": "Task deleted"}

