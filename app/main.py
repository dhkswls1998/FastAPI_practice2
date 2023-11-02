from fastapi import FastAPI
from app.database.sqlite import engine
from app.routers import router_user
#from app.routers import router_vegetable
#from app.routers import router_garden

app = FastAPI()

# 데이터베이스 초기화
from app.database.crud_user import Base as UserBase
#from app.database.crud_vegetable import Base as VegetableBase
#from app.database.crud_garden import Base as GardenBase

UserBase.metadata.create_all(bind=engine)
#VegetableBase.metadata.create_all(bind=engine)
#GardenBase.metadata.create_all(bind=engine)

# 라우터 등록
app.include_router(router_user.router)
#app.include_router(router_vegetable.router)
#app.include_router(router_garden.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)