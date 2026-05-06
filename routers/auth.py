from config import SECRET_KEY, ALGORITHM
from dotenv import load_dotenv
load_dotenv()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

from database import get_db
from models.user import User
from fastapi import Form, Response
from fastapi.responses import RedirectResponse

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ======================
# TOKEN
# ======================

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": int(expire.timestamp())})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ======================
# PASSWORD
# ======================

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# ======================
# REGISTER
# ======================

@router.post("/register")
def register(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(User.email == email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        email=email,
        password=hash_password(password)
    )

    db.add(user)
    db.commit()

    return RedirectResponse(url="/login", status_code=303)


# ======================
# LOGIN
# ======================

@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == username).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    response = RedirectResponse(url="/clients-page", status_code=303)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        samesite="lax"
    )

    return response