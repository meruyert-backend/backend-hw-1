from sqlalchemy.orm import Session
from models.client import Client
from models.communication import Communication
from models.task import Task



#СОЗДАНИЕ
def create_client(db: Session, name: str, company: str, notes: str, user_id: int):
    client = Client(
        name=name,
        company=company,
        notes=notes,
        user_id=user_id
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    return client

#ПОЛУЧИТЬ ВСЕХ КЛИЕНТОВ ПОЛЬЗОВАТЕЛЯ
def get_clients(db: Session, user_id: int):
    return db.query(Client).filter(Client.user_id == user_id).all()


#ПОЛУЧИТЬ ОДНОГО
def get_client(db: Session, client_id: int, user_id: int):
    return db.query(Client).filter(
        Client.id == client_id,
        Client.user_id == user_id
    ).first()


#ОБНОВИТЬ
def update_client(db: Session, client: Client, name: str, company: str, notes: str):
    client.name = name
    client.company = company
    client.notes = notes

    db.commit()
    db.refresh(client)

    return client


#УДАЛИТЬ
def delete_client(db: Session, client: Client):
    # удалить tasks
    db.query(Task).filter(Task.client_id == client.id).delete()

    # удалить communications
    db.query(Communication).filter(Communication.client_id == client.id).delete()

    db.delete(client)
    db.commit()