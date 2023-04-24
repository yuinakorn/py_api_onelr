from fastapi import FastAPI

from models.pregs.pregs_model import PregBase, PregDisplayBase
from routers import pregs_router
# from routers.auth import authen_router
# from routers.items import items_router
from models.database import engine

app = FastAPI()

app.include_router(pregs_router.router)

