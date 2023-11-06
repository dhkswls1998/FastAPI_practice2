# router_vegetable.py

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.database.model import User, Vegetable
from app.schemas.schema_user import UserCreate, User as UserPydantic
from app.schemas.schema_vegetable import VegetableCreate, Vegetable as VegetablePydantic
from typing import List
import json

router = APIRouter()

# SQLAlchemy 모델 (Vegetable) -> Pydantic 모델 (VegetablePydantic)
def sqlalchemy_to_pydantic(vegetable: Vegetable) -> VegetablePydantic:

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
        vegetableDate=vegetable_data.vegetableDate,
        owner_id=current_user.id  # owner를 현재 사용자로 설정
    )
    
    # vegetableAge를 계산하고 업데이트
    new_vegetable.calculate_vegetable_age()

    db.add(new_vegetable)
    db.commit()
    db.refresh(new_vegetable)

    # User 모델의 ownedVegetableIDs에 추가
    ownedVegetableIDs = current_user.get_owned_vegetable_ids()
    ownedVegetableIDs.append(new_vegetable.id)
    current_user.set_owned_vegetable_ids(ownedVegetableIDs)
    db.commit()
    db.refresh(current_user)
    
    return sqlalchemy_to_pydantic(new_vegetable)

# 식물 정보 엔드포인트
@router.get("/me/{vegetableID}", response_model=List[VegetablePydantic])
def get_owned_vegetable_by_id(vegetableID: int, db: Session = Depends(get_db)):

    # 현재 사용자 ID 가져오기
    current_user = db.query(User).order_by(User.login_time.desc()).first()

    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")

    if vegetableID not in current_user.get_owned_vegetable_ids():
        raise HTTPException(status_code=404, detail="Vegetable not found")

    # 데이터베이스에서 vegetableID에 해당하는 정보 가져오기
    temp_vegetable_data = db.query(Vegetable).filter(Vegetable.id == vegetableID).first()

    if not temp_vegetable_data:
        raise HTTPException(status_code=404, detail="Vegetable not found")

    return [sqlalchemy_to_pydantic(temp_vegetable_data)]

# 식물 목록 '확인' 엔드포인트 : Ex. owned_ids = [ 1, 2 ]
@router.get("/me/ownedIDs", response_model=List[int])
def get_owned_ids(db: Session = Depends(get_db)):

    # 현재 사용자 ID 가져오기
    current_user = db.query(User).order_by(User.login_time.desc()).first()

    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")

    # 사용자가 소유한 vegetableID들을 반환
    owned_ids = current_user.get_owned_vegetable_ids()

    return owned_ids