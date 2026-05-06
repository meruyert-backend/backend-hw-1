from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models.user import User

from repositories import client_repo, task_repo
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/clients-page", response_class=HTMLResponse)
def clients_page(
    request: Request,
    db: Session = Depends(get_db),
):
    clients = client_repo.get_clients(db, user_id=1)

    print("TYPE:", type(clients))
    print("FIRST:", clients[0] if clients else "EMPTY")

    return templates.TemplateResponse(
        request=request,
        name="clients.html",
        context={
            "clients": clients
        }
    )


@router.get("/tasks-page", response_class=HTMLResponse)
def tasks_page(
    request: Request,
    db: Session = Depends(get_db),
):
    tasks = task_repo.get_tasks(db, user_id=1)

    return templates.TemplateResponse(
        request=request,
        name="tasks.html",
        context={
            "tasks": tasks
        }
    )