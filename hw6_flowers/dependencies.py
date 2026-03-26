from fastapi import Request
from database import SessionLocal
import models
from auth import decode_token


def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        return None

    payload = decode_token(token)

    if not payload:
        return None

    user_id = payload.get("user_id")

    db = SessionLocal()
    user = db.query(models.User).filter(models.User.id == user_id).first()

    return user