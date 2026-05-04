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

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(tasks.router)
app.include_router(communications.router)
app.include_router(pages.router)


