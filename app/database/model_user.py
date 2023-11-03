# model_user.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.sqlite import Base
from datetime import datetime
import json

class User(Base):
    __tablename__ = "UserID"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    age = Column(Integer)
    # JSON 문자열로 저장
    ownedVegetableIDs = Column(String, default="[]", server_default="[]")
    login_time = Column(DateTime, default=datetime.utcnow)

    # OwnedVegetables 관계 설정
    ownedVegetables = relationship("Vegetable", back_populates="owner")

    def set_owned_vegetable_ids(self, vegetable_ids):
        # Python 리스트를 JSON 문자열로 변환하여 열에 저장
        self.ownedVegetableIDs = json.dumps(vegetable_ids)

    def get_owned_vegetable_ids(self):
        # JSON 문자열을 파싱하여 Python 리스트로 반환
        return json.loads(self.ownedVegetableIDs) if self.ownedVegetableIDs else []

from app.database.model_vegetable import Vegetable