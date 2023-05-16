import jwt
import logging
import requests
from dotenv import dotenv_values
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from models.pregs.pregs_model import DbPreg

config_env = dotenv_values(".env")


def token_decode(token):
    secret_key = config_env["SECRET_KEY"]
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=[config_env["ALGORITHM"]])
        return {"token_data": decoded_token, "is_valid": True}

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"status": "error", "message": "Token is invalid!!"})


def read_preg(request, db: Session):
    token = request.get("token")
    if token_decode(token)['is_valid']:
        return db.query(DbPreg).filter(DbPreg.hcode == token_decode(token)['token_data']['hosCode']).all()

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"status": "error", "message": "You are not allowed!!"})


def search(db: Session, request):
    token = request.get("token")

    if token_decode(token)['is_valid']:
        result = db.query(DbPreg).filter(DbPreg.hcode == token_decode(token)['token_data']['hosCode'],
                                         DbPreg.cid == request.get("cid"), DbPreg.an == request.get("an")).first()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={
                    "status": "error",
                    "message": f"ไม่พบข้อมูลของ an {request.get('an')} ในระบบ"
                }
            )
        else:
            return result

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"status": "error", "message": "You are not allowed!!"})


def his_search(request):
    token = request.get("token")

    if token_decode(token)['is_valid']:
        auth = {}
        api_url = f"{config_env['HIS_URL']}/person_anc/{request.get('hcode')}?cid={request.get('cid')}"
        response = requests.get(api_url, auth=auth)
        result = response.json()

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={
                    "status": "error",
                    "message": f"ไม่พบข้อมูลของ an {request.get('an')} ในระบบ"
                }
            )
        else:
            return result

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"status": "error", "message": "You are not allowed!!"})


def token_check(request):
    token = request.get("token")
    secret_key = config_env["SECRET_KEY"]
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_data = {
            "hoscode": decoded_token["hosCode"],
            "username": decoded_token["username"],
            "user_cid": decoded_token["cid"]
        }
        # print(user_data)
        message = "Token is valid"
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"status": "ok", "message": message, "data": user_data})

    except jwt.InvalidTokenError:
        message = "Token is invalid!!"
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"status": "error", "message": message})


def create(db: Session, request):
    token = request.get("token")
    if token_decode(token)['is_valid']:
        current_date = datetime.now()
        new_preg = DbPreg(
            hcode=token_decode(token)['token_data']['hosCode'],
            cid=request.cid,
            hn=request.hn,
            an=request.an,
            admit_date=request.admit_date,
            pname=request.pname,
            lname=request.lname,
            age_y=request.age_y,
            gravida=request.gravida,
            parity=request.parity,
            ga=request.ga,
            anc_check_up=request.anc_check_up,
            no_of_anc=request.no_of_anc,
            weight_before_pregancy=request.weight_before_pregancy,
            weight_at_delivery=request.weight_at_delivery,
            weight_gain=request.weight_gain,
            height=request.height,
            fundal_height=request.fundal_height,
            hematocrit=request.hematocrit,
            ultrasound=request.ultrasound,
            cpd_risk_score=request.cpd_risk_score,
            status=request.status,
            create_date=current_date,
            modify_date=request.modify_date,
            user_create=request.user_create,
            user_last_modify=request.user_last_modify
        )
        try:
            db.add(new_preg)
            db.commit()
            db.refresh(new_preg)
            return {"message": "ok", "detail": new_preg}
        except SQLAlchemyError as e:
            db.rollback()
            error_message = f"Error creating preg: {str(e)}"
            logging.error(error_message)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={"status": "error", "message": error_message})

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"status": "error", "message": "You are not allowed!!"})


def update(db: Session, request):
    token = request.get("token")
    if token_decode(token)['is_valid']:
        result = db.query(DbPreg).filter(DbPreg.hcode == token_decode(token)['token_data']['hosCode'],
                                         DbPreg.cid == request.cid,
                                         DbPreg.an == request.an).first()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={
                    "status": "error",
                    "message": f"ไม่พบข้อมูลของ an {request.an}"
                }
            )
        else:
            now = datetime.now()
            modify_date = now.strftime("%Y-%m-%d %H:%M:%S")
            result.hcode = token_decode(token)['token_data']['hosCode']
            result.cid = request.cid
            result.hn = request.hn
            result.an = request.an
            result.admit_date = request.admit_date
            result.pname = request.pname
            result.lname = request.lname
            result.age_y = request.age_y
            result.gravida = request.gravida
            result.parity = request.parity
            result.ga = request.ga
            result.anc_check_up = request.anc_check_up
            result.no_of_anc = request.no_of_anc
            result.weight_before_pregancy = request.weight_before_pregancy
            result.weight_at_delivery = request.weight_at_delivery
            result.weight_gain = request.weight_gain
            result.height = request.height
            result.fundal_height = request.fundal_height
            result.hematocrit = request.hematocrit
            result.ultrasound = request.ultrasound
            result.cpd_risk_score = request.cpd_risk_score
            result.status = request.status
            result.modify_date = modify_date
            result.user_last_modify = request.user_last_modify

            try:
                db.commit()
                db.refresh(result)
                return {"message": "ok", "detail": result}
            except SQLAlchemyError as e:
                db.rollback()
                error_message = f"Error updating preg: {str(e)}"
                logging.error(error_message)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail={"status": "error", "message": error_message})

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"status": "error", "message": "You are not allowed!!"})


def delete(db: Session, request):
    token = request.get("token")
    if token_decode(token)['is_valid']:
        result = db.query(DbPreg).filter(DbPreg.hcode == token_decode(token)['token_data']['hosCode'],
                                         DbPreg.cid == request.cid,
                                         DbPreg.an == request.an).first()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={
                    "status": "error",
                    "message": f"ไม่พบข้อมูลของ an {request.an}"
                }
            )
        else:
            try:
                db.delete(result)
                db.commit()
                return {"message": "ok", "detail": result}
            except SQLAlchemyError as e:
                db.rollback()
                error_message = f"Error deleting preg: {str(e)}"
                logging.error(error_message)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail={"status": "error", "message": error_message})

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"status": "error", "message": "You are not allowed!!"})
