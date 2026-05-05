from sqlalchemy.orm import Session
from models.task import Task

#CREATE
def create_task(db: Session, title: str, deadline: str, client_id: int, communication_id: int = None):
    task = Task(
        title=title,
        deadline=deadline,
        client_id=client_id,
        communication_id=communication_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


#GET ALL (по пользователю)
def get_tasks(db: Session, user_id: int):
    return db.query(Task).join(Task.client).filter(
        Task.client.has(user_id=user_id)
    ).all()


#GET ONE
def get_task(db: Session, task_id: int, user_id: int):
    return db.query(Task).join(Task.client).filter(
        Task.client_id == Client.id,
        Client.user_id == user_id
    ).all()

#UPDAT
def update_task(db: Session, task: Task, title: str, deadline: str, status: str):
    task.title = title
    task.deadline = deadline
    task.status = status

    db.commit()
    db.refresh(task)

    return task


#DELETE
def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()
