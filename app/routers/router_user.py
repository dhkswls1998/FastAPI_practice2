# router_user.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.database.model_user import User
from app.schemas.schema_user import UserCreate, User as UserPydantic
from app.routers import router_vegetable
from datetime import datetime
from fastapi import Query
from fastapi.responses import RedirectResponse

router = APIRouter()

# SQLAlchemy 모델 (User) -> Pydantic 모델 (UserPydantic)
def sqlalchemy_to_pydantic(user: User) -> UserPydantic:
    return UserPydantic(
        username=user.username,
        name=user.name,
        age=user.age,
        ownedVegetableIDs=user.get_owned_vegetable_ids()
    )

# 회원가입 엔드포인트
@router.post("/register", response_model=UserPydantic)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        password=user.password,
        name=user.name,
        age=user.age,
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return sqlalchemy_to_pydantic(db_user)

# 로그인 엔드포인트
@router.post("/login", response_model=UserPydantic)
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user is None or user.password != password:
        raise HTTPException(status_code=401, detail="Login failed")
    user.login_time = datetime.utcnow()
    db.commit()
    return sqlalchemy_to_pydantic(user)

# 가장 최근에 로그인한 사용자 정보를 가져오도록 수정
@router.get("/me", response_model=UserPydantic)
def get_current_authenticated_user(
    db: Session = Depends(get_db),
    redirect: bool = Query(False, description="Automatically redirect based on owned vegetable IDs")
):
    user = db.query(User).order_by(User.login_time.desc()).first()

    if redirect:
        # 사용자가 가진 vegetableIDs 목록 가져오기
        owned_vegetable_ids = user.get_owned_vegetable_ids()

        if not owned_vegetable_ids:
            # 사용자가 가진 vegetableID가 없을 때, /me/plant로 리다이렉트
            return RedirectResponse(url='/me/plant')
        elif len(owned_vegetable_ids) == 1:
            # 사용자가 가진 vegetableID가 하나일 때, 해당 vegetableID로 리다이렉트
            return RedirectResponse(url=f'/me/{owned_vegetable_ids[0]}')
        else:
            # 사용자가 가진 vegetableID가 여러 개일 때, /me/ownedIDs로 리다이렉트
            return RedirectResponse(url='/me/ownedIDs')

    return sqlalchemy_to_pydantic(user)