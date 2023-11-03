# schema_vegetable.py

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

# 사용 가능한 Type과 Char 선택지 정의
class VegetableType(str, Enum):
    TypeA = "TypeA"
    TypeB = "TypeB"
    TypeC = "TypeC"
    TypeD = "TypeD"

class VegetableChar(str, Enum):
    CharA = "CharA"
    CharB = "CharB"
    CharC = "CharC"
    CharD = "CharD"

# 식물 등록 요청
class VegetableCreate(BaseModel):
    vegetableName: str
    vegetableType: VegetableType = Field(..., description="Type 선택: TypeA, TypeB, TypeC, TypeD")
    vegetableChar: VegetableChar = Field(..., description="Char 선택: CharA, CharB, CharC, CharD")

# 식물 정보 응답 처리
class Vegetable(BaseModel):
    id: int
    vegetableName: str
    vegetableType: VegetableType
    vegetableChar: VegetableChar
    vegetableLevel: int
    vegetableDate: datetime
    vegetableAge: int

    class Config:
        from_attributes = True
