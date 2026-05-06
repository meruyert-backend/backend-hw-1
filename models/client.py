from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    company = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    user = relationship("User", back_populates="clients")
    communications = relationship("Communication", back_populates="client")
    tasks = relationship("Task", back_populates="client", cascade="all, delete")