from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from database import get_db
from repositories import client_repo, task_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/clients-page", response_class=HTMLResponse)
def clients_page(request: Request, db: Session = Depends(get_db)):
    clients = client_repo.get_clients(db)

    return templates.TemplateResponse(
        "clients.html",
        {
            "request": request,
            "clients": clients
        }
    )


@router.get("/tasks-page", response_class=HTMLResponse)
def tasks_page(request: Request, db: Session = Depends(get_db)):
    tasks = task_repo.get_tasks(db)

    return templates.TemplateResponse(
        "tasks.html",
        {
            "request": request,
            "tasks": tasks
        }
    )