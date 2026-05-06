from sqlalchemy.orm import Session
from models.communication import Communication
from services.ai_service import extract_tasks
from repositories import task_repo

#CREATE
def create_communication(
    db,
    text,
    client_id,
):
    communication = Communication(
        text=text,
        client_id=client_id
    )

    db.add(communication)
    db.commit()
    db.refresh(communication)

    # 🔥 AI PART
    tasks = extract_tasks(text)

    print("AI RESULT:", tasks)

    for t in tasks:
        if "title" not in t:
            continue

        task_repo.create_task(
            db=db,
            title=t["title"],
            deadline=t.get("deadline"),
            client_id=client_id,
            communication_id=communication.id
        )

    return communication


#GET ALL (по пользователю)
def get_communications(db: Session, user_id: int):
    return db.query(Communication).join(Communication.client).filter(
        Communication.client.has(user_id=user_id)
    ).all()

#GET ONE
def get_communication(db: Session, comm_id: int, user_id: int):
    return db.query(Communication).join(Communication.client).filter(
        Communication.id == comm_id,
        Communication.client.has(user_id=user_id)
    ).first()

#DELETE
def delete_communication(db: Session, comm: Communication):
    db.delete(comm)
    db.commit()

