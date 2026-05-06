from config import SECRET_KEY, ALGORITHM
from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models.user import User

from dotenv import load_dotenv
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # remove "Bearer "
    token = token.replace("Bearer ", "")

    user_id = decode_token(token)

    return db.query(User).filter(User.id == user_id).first()