from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from config import SECRET_KEY, ALGORITHM
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from database import engine, Base
from routers import clients, tasks, communications, pages, auth
import models.user
import models.client
import models.communication
import models.task

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(tasks.router)
app.include_router(communications.router)
app.include_router(pages.router)


