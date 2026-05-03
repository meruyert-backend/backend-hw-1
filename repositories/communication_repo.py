from sqlalchemy.orm import Session
from models.communication import Communication

#CREATE
def create_communication(db: Session, text: str, client_id: int):
    comm = Communication(
        text=text,
        client_id=client_id
    )

    db.add(comm)
    db.commit()
    db.refresh(comm)

    return comm


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

