import jwt
import logging
from dotenv import dotenv_values
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from models.progress.progress_model import DbProgress

config_env = dotenv_values(".env")


def token_decode(token):
    secret_key = config_env["SECRET_KEY"]
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=[config_env["ALGORITHM"]])
        return {"token_data": decoded_token, "is_valid": True}

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"status": "error", "message": "Token is invalid!!"})


def read_progress(request, db: Session):
    token = request.get("token")
    if token_decode(token)['is_valid']:
        return db.query(DbProgress).filter(DbProgress.hcode == token_decode(token)['token_data']['hosCode']).all()

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"status": "error", "message": "You are not allowed!!"})


def search(db: Session, request):
    token = request.get("token")

    if token_decode(token)['is_valid']:
        result = db.query(DbProgress).filter(DbProgress.hcode == token_decode(token)['token_data']['hosCode'],
                                             DbProgress.cid == request.get("cid"),
                                             DbProgress.an == request.get("an")).all()
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
    token = request.token
    if token_decode(token)['is_valid']:
        new_progress = DbProgress(
            hcode=token_decode(token)['token_data']['hosCode'],
            cid=request.cid,
            hn=request.hn,
            an=request.an,
            progress_date_time=request.progress_date_time,
            code=request.code,
            value=request.value,
            comment=request.comment
        )
        try:
            db.add(new_progress)
            db.commit()
            db.refresh(new_progress)
            return {"message": "ok", "detail": new_progress}
        except SQLAlchemyError as e:
            db.rollback()
            error_message = f"Error creating Progress: {str(e)}"
            logging.error(error_message)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail={"status": "error", "message": error_message})

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"status": "error", "message": "You are not allowed!!"})


def update(db: Session, request):
    token = request.get("token")
    if token_decode(token)['is_valid']:
        result = db.query(DbProgress).filter(DbProgress.hcode == token_decode(token)['token_data']['hosCode'],
                                             DbProgress.cid == request.cid,
                                             DbProgress.an == request.an).first()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={
                    "status": "error",
                    "message": f"ไม่พบข้อมูลของ an {request.an}"
                }
            )
        else:
            # now = datetime.now()
            # modify_date = now.strftime("%Y-%m-%d %H:%M:%S")
            result.hcode = token_decode(token)['token_data']['hosCode']
            result.cid = request.cid
            result.hn = request.hn
            result.an = request.an
            result.progress_date_time = request.progress_date_time
            result.code = request.code
            result.value = request.value
            result.comment = request.comment

            try:
                db.commit()
                db.refresh(result)
                return {"message": "ok", "detail": result}
            except SQLAlchemyError as e:
                db.rollback()
                error_message = f"Error updating Progress: {str(e)}"
                logging.error(error_message)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail={"status": "error", "message": error_message})

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"status": "error", "message": "You are not allowed!!"})


def delete(db: Session, request):
    token = request.get("token")
    if token_decode(token)['is_valid']:
        result = db.query(DbProgress).filter(DbProgress.hcode == token_decode(token)['token_data']['hosCode'],
                                             DbProgress.cid == request.cid,
                                             DbProgress.an == request.an).first()
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
                error_message = f"Error deleting Progress: {str(e)}"
                logging.error(error_message)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail={"status": "error", "message": error_message})

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail={"status": "error", "message": "You are not allowed!!"})