from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Communication(Base):
    __tablename__ = "communications"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    text = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="communications")
    tasks = relationship("Task", back_populates="communication")