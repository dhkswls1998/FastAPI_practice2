# router_garden.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.sqlite import get_db
from app.database.model import GardenBase
from app.schemas.schema_garden import GardenCreate, Garden

router = APIRouter()

# 텃밭 정보 엔드포인트
@router.post("/garden", response_model=Garden)
def update_garden_data(garden_data: GardenCreate, db: Session = Depends(get_db)):
    garden = GardenBase(**garden_data.dict())

    db.add(garden)
    db.commit()
    db.refresh(garden)

    return garden