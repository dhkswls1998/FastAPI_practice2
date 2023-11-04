# router_vegetable.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.database.model_user import User
from app.schemas.schema_user import UserCreate, User as UserPydantic
from app.database.model_vegetable import Vegetable
from app.schemas.schema_vegetable import VegetableCreate, Vegetable as VegetablePydantic
from fastapi import Query
from typing import List
import json

router = APIRouter()

# SQLAlchemy 모델 (Vegetable) -> Pydantic 모델 (Vegetable)
def sqlalchemy_to_pydantic_vegetable(vegetable: Vegetable) -> VegetablePydantic:
    return VegetablePydantic(
        id=vegetable.id,
        vegetableName=vegetable.vegetableName,
        vegetableType=vegetable.vegetableType,
        vegetableChar=vegetable.vegetableChar,
        vegetableLevel=vegetable.vegetableLevel,
        vegetableDate=vegetable.vegetableDate,
        vegetableAge=vegetable.vegetableAge
    )

# 식물 등록 엔드포인트
@router.post("/me/plant", response_model=VegetablePydantic)
def register_plant(vegetable_data: VegetableCreate, db: Session = Depends(get_db)):
    # 현재 사용자 ID 가져오기
    current_user = db.query(User).order_by(User.login_time.desc()).first()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # 새로운 식물 생성 (고유 id는 자동으로 생성)
    new_vegetable = Vegetable(
        vegetableName=vegetable_data.vegetableName,
        vegetableType=vegetable_data.vegetableType,
        vegetableChar=vegetable_data.vegetableChar,
        owner=current_user  # owner를 현재 사용자로 설정
    )
    db.add(new_vegetable)
    db.commit()
    db.refresh(new_vegetable)

    # User 모델의 ownedVegetableIDs에 추가
    owned_vegetables = current_user.get_owned_vegetable_ids()
    owned_vegetables.append(new_vegetable.id)
    current_user.set_owned_vegetable_ids(owned_vegetables)
    db.commit()
    db.refresh(current_user)
    
    return sqlalchemy_to_pydantic_vegetable(new_vegetable)

# 가장 최근에 로그인한 사용자 정보를 가져오도록 수정
@router.get("/me/{vegetableID}", response_model=List[VegetablePydantic])
def get_owned_vegetable_by_id(vegetableID: int, db: Session = Depends(get_db)):
    # 현재 사용자 ID 가져오기
    current_user = db.query(User).order_by(User.login_time.desc()).first()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # 사용자의 소유한 식물들 중 vegetableID와 일치하는 것을 찾아 반환
    owned_vegetables = current_user.get_owned_vegetable_ids()
    if vegetableID not in owned_vegetables:
        raise HTTPException(status_code=404, detail="Vegetable not found")

    vegetable_data = []
    # 데이터베이스에서 vegetableID에 해당하는 정보 가져오기
    for id in owned_vegetables:
        if id == vegetableID:
            # Vegetable 모델을 이용해 데이터베이스에서 정보 가져오기
            vegetable = db.query(Vegetable).filter(Vegetable.id == vegetableID).first()
            if vegetable:
                vegetable_data.append(sqlalchemy_to_pydantic_vegetable(vegetable))

    return vegetable_data

# 사용자의 모든 vegetableID 조회
@router.get("/me/ownedIDs", response_model=List[int])
def get_owned_vegetable_ids(db: Session = Depends(get_db)):
    # 현재 사용자 ID 가져오기
    current_user = db.query(User).order_by(User.login_time.desc()).first()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # 사용자의 소유한 vegetableID 목록 가져오기 (문자열로 저장된 JSON을 파싱하여 리스트로 변환)
    owned_vegetable_ids_str = current_user.ownedVegetableIDs
    owned_vegetable_ids = json.loads(owned_vegetable_ids_str) if owned_vegetable_ids_str else []
    
    return owned_vegetable_ids