from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from models.database import get_db
from models.pregs.pregs_model import PregBase, PregDisplayBase, LoginBase, CreateBase
from controllers import dashboard_controller

# from utils.oauth2 import access_user_token

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/hospitals/")
def read_hostpitals():
    return dashboard_controller.read_hostpitals()


@router.post("/hospitals/")
def read_dashboard_all():
    return dashboard_controller.read_dashboard_all()


@router.post("/hospital/{hcode}")
def read_hospital_by_hcode(hcode: str):
    return dashboard_controller.read_hospital_by_hcode(hcode)


@router.post("/chart/{hcode}/{an}")
def read_chart_by_an(hcode: str, an: str):
    return dashboard_controller.read_hospital_by_an(hcode, an)
