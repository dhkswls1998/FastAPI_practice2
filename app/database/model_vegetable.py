# model_vegetable.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.sqlite import Base
from datetime import datetime
from app.database.model_user import User

class Vegetable(Base):
    __tablename__ = "VegetableID"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    vegetableName = Column(String)
    vegetableType = Column(String)
    vegetableChar = Column(String)
    vegetableLevel = Column(Integer, default=2)
    vegetableDate = Column(DateTime, default=datetime.utcnow)
    vegetableAge = Column(Integer, default=1)
    owner_id = Column(Integer, ForeignKey("UserID.id"))