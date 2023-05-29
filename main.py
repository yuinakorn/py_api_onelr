from fastapi import FastAPI

from models.pregs.pregs_model import PregBase, PregDisplayBase
from routers import pregs_router, infants_router, dashboard_router, progress_router
# from routers import dashboard_router
# from routers import progress_router

# from routers.auth import authen_router
# from routers.items import items_router
from models.database import engine

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pregs_router.router)
app.include_router(infants_router.router)
app.include_router(progress_router.router)
app.include_router(dashboard_router.router)

