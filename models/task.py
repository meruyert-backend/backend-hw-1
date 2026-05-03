from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    communication_id = Column(Integer, ForeignKey("communications.id"), nullable=True)

    title = Column(String, nullable=False)
    deadline = Column(String, nullable=True)
    status = Column(String, default="todo")

    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="tasks")
    communication = relationship("Communication", back_populates="tasks")