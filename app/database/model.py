# model.py

from sqlalchemy import Column, Integer, Float, String, LargeBinary, DateTime, ForeignKey
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

    def get_owned_vegetable_ids(self):
        # JSON 문자열을 파싱하여 Python 리스트로 반환
        return json.loads(self.ownedVegetableIDs) if self.ownedVegetableIDs else []

    def set_owned_vegetable_ids(self, new_vegetable_id):
        # Python 리스트를 JSON 문자열로 변환하여 열에 저장
        self.ownedVegetableIDs = json.dumps(new_vegetable_id)

class Vegetable(Base):
    __tablename__ = "VegetableID"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    vegetableName = Column(String)
    vegetableType = Column(String)
    vegetableChar = Column(String)
    vegetableLevel = Column(Integer, default=2)
    vegetableDate = Column(String)
    vegetableAge = Column(Integer)
    owner_id = Column(Integer, ForeignKey("UserID.id"))

    def calculate_vegetable_age(self):
        if self.vegetableDate:
            temp_vegetable_date = datetime.strptime(self.vegetableDate, "%Y-%m-%d")
            vegetable_month = temp_vegetable_date.month
            vegetable_date = temp_vegetable_date.date()

            temp_current_date = datetime.utcnow()
            current_month = temp_current_date.month
            current_date = temp_current_date.date()

            if vegetable_month == current_month:
                vegetable_age = (current_date - vegetable_date).days
            else:
                if vegetable_month < current_month:
                    if vegetable_month == 10 and current_month == 11:
                        vegetable_age = (31 - vegetable_date.day) + current_date.day
                    elif vegetable_month == 11 and current_month == 12:
                        vegetable_age = (30 - vegetable_date.day) + current_date.day
                    elif vegetable_month == 10 and current_month == 12:
                        vegetable_age = (31 - vegetable_date.day) + 30 + current_date.day
                    else:
                        vegetable_age = 0
                else:
                    vegetable_age = 0

            if vegetable_age >= 0:
                self.vegetableAge = vegetable_age

class GardenBase(Base):
    __tablename__ = "Garden"
    id = Column(Integer, primary_key=True, index=True)
    gardenTemp = Column(Float, default=25.0)
    gardenHumid = Column(Float, default=50.0)
    gardenWater = Column(Integer, default=60)
    gardenImage = Column(LargeBinary, default="/app/database/default_image.png")