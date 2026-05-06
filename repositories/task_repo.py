from sqlalchemy.orm import Session
from models.task import Task
from models.client import Client


def create_task(
    db,
    title,
    deadline,
    client_id,
    user_id,
    communication_id=None
):
    task = Task(
        title=title,
        deadline=deadline,
        client_id=client_id,
        user_id=user_id,
        communication_id=communication_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task



def get_tasks(db, user_id: int):
    return db.query(Task).join(Task.client).filter(
        Client.user_id == user_id
    ).all()


def get_task(db: Session, task_id: int, user_id: int):
    return db.query(Task).join(Task.client).filter(
        Task.id == task_id,
        Client.user_id == user_id
    ).first()


def update_task(db: Session, task: Task, title: str, deadline: str, status: str):
    task.title = title
    task.deadline = deadline
    task.status = status

    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()
