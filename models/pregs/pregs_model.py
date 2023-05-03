from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime

from models.database import Base
from pydantic import BaseModel
from typing import Optional


class DbPreg(Base):
    __tablename__ = "t_pregancy"
    hcode = Column(String, primary_key=True, index=True)
    cid = Column(String, primary_key=True, index=True)
    hn = Column(String)
    an = Column(String, primary_key=True, index=True)
    admit_date = Column(DateTime, nullable=True)
    pname = Column(String)
    lname = Column(String)
    age_y = Column(String)
    gravida = Column(String)
    parity = Column(String)
    ga = Column(String)
    anc_check_up = Column(String)
    no_of_anc = Column(String)
    weight_before_pregancy = Column(String)
    weight_at_delivery = Column(String)
    weight_gain = Column(String)
    height = Column(String)
    fundal_height = Column(String)
    hematocrit = Column(String)
    ultrasound = Column(String)
    cpd_risk_score = Column(String, nullable=True)
    status = Column(Integer)
    create_date = Column(DateTime, nullable=True)
    modify_date = Column(DateTime, nullable=True)
    user_create = Column(String, nullable=True)
    user_last_modify = Column(String, nullable=True)


class PregBase(BaseModel):
    token: str
    # hcode: str
    cid: str
    an: str

    class Config:
        orm_mode = True

    def get(self, key):
        return getattr(self, key, None)


class PregDisplayBase(BaseModel):
    hcode: str
    cid: str
    hn: str
    an: str
    admit_date: Optional[datetime] = None
    pname: str
    lname: str
    age_y: str
    gravida: str
    parity: str
    ga: str
    anc_check_up: str
    no_of_anc: str
    weight_before_pregancy: str
    weight_at_delivery: str
    weight_gain: str
    height: str
    fundal_height: str
    hematocrit: str
    ultrasound: str
    cpd_risk_score: Optional[str] = None
    status: int
    create_date: datetime
    modify_date: Optional[datetime] = None
    user_create: Optional[str] = None
    user_last_modify: Optional[str] = None

    class Config:
        orm_mode = True


class LoginBase(BaseModel):
    token: str

    class Config:
        orm_mode = True

    def get(self, key):
        return getattr(self, key, None)


class CreateBase(BaseModel):
    token: str
    # hcode: str
    cid: str
    hn: str
    an: str
    admit_date: datetime
    pname: str
    lname: str
    age_y: str
    gravida: str
    parity: str
    ga: str
    anc_check_up: str
    no_of_anc: str
    weight_before_pregancy: str
    weight_at_delivery: str
    weight_gain: str
    height: str
    fundal_height: str
    hematocrit: str
    ultrasound: str
    cpd_risk_score: Optional[str] = None
    status: int
    create_date: datetime
    modify_date: datetime
    user_create: Optional[str] = None
    user_last_modify: Optional[str] = None

    class Config:
        orm_mode = True

    def get(self, key):
        return getattr(self, key, None)

