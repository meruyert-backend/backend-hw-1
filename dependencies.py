from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from routers.auth import decode_access_token


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # remove "Bearer "
    token = token.replace("Bearer ", "")

    # decode token → returns dict
    payload = decode_access_token(token)

    # extract email (you stored it as "sub")
    email = payload.get("sub")

    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    # find user by email (NOT id)
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user