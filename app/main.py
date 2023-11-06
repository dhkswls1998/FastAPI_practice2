# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.sqlite import engine
from app.routers import router_user
from app.routers import router_vegetable
from app.routers import router_garden

app = FastAPI()

# CORS 설정 : local test -> 주석처리 변경
# origins = ["http://localhost:8080"]
origins = ["http://59.5.235.142:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.database.model import Base as UserBase
from app.database.model import Base as VegetableBase
from app.database.model import Base as GardenBase

UserBase.metadata.create_all(bind=engine)
VegetableBase.metadata.create_all(bind=engine)
GardenBase.metadata.create_all(bind=engine)

app.include_router(router_user.router)
app.include_router(router_vegetable.router)
app.include_router(router_garden.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)