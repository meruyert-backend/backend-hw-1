from fastapi import FastAPI

from database import engine, Base
from routers import clients, tasks, communications, pages

from models import user, client, communication, task

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(clients.router)
app.include_router(tasks.router)
app.include_router(communications.router)
app.include_router(pages.router)


