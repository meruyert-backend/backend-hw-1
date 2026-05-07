from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from database import get_db
from repositories import client_repo, task_repo, communication_repo

from dependencies import get_current_user
from models.user import User

from fastapi import Form
from schemas.client import ClientResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")



@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context={}
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        name="login.html",
        request=request,
        context={}
    )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        name="register.html",
        request=request,
        context={}
    )


@router.get("/clients-page")
def clients_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    clients = client_repo.get_clients(db, current_user.id)

    return templates.TemplateResponse(
        name="clients.html",
        request=request,
        context={
            "request": request,
            "clients": clients
        }
    )

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


#GET ONE
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = task_repo.get_task(db, task_id, current_user.id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.get("/tasks-page", response_class=HTMLResponse)
def tasks_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = task_repo.get_tasks(db, current_user.id)

    return templates.TemplateResponse(
        name="tasks.html",
        request=request,
        context={
            "request": request,
            "tasks": tasks
        }
    )


@router.get("/tasks/form")
def task_form(request: Request):
    return templates.TemplateResponse(
        "tasks.html",
        {"request": request}
    )


@router.get("/communications-page")
def communications_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    communications = communication_repo.get_communications(db, current_user.id)

    return templates.TemplateResponse(
        name="communications.html",
        request=request,
        context={
            "request": request,
            "communications": communications
        }
    )


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


@router.get("/communications/form")
def communications_form_page(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "communications.html",
        {
            "request": request,
            "user": current_user
        }
    )


