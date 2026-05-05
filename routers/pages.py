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
    current_user: User = Depends(get_current_user)
):
    clients = client_repo.get_clients(db, current_user.id)

    print("TYPE:", type(clients))
    print("FIRST:", clients[0] if clients else "EMPTY")

    return templates.TemplateResponse("clients.html", {
        "request": request,
        "clients": clients
    })


@router.get("/tasks-page", response_class=HTMLResponse)
def tasks_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = task_repo.get_tasks(db, current_user.id)

    return templates.TemplateResponse("tasks.html", {
        "request": request,
        "tasks": tasks
    })