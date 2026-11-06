from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError
import bcrypt
import os

# Adjust these imports to match your project structure
from backend.db.db import get_db
from backend.models.models import User
from backend.schema.schema import UserCreate, UserLogin, Token

# --- JWT Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 3))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


# --- Helper Functions ---
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# --- Routes ---
@auth_router.post("/register", response_model=Token)
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.email == body.email) | (User.username == body.username)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")

    # bcrypt requires bytes
    hashed_password = bcrypt.hashpw(body.password.encode("utf-8"), bcrypt.gensalt())

    user = User(
        username=body.username,
        email=body.email,
        hashed_password=hashed_password.decode("utf-8"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/login", response_model=Token)
def login_user(body: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.email == body.username_or_email) | (User.username == body.username_or_email)
    ).first()
    
    if not existing_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    
    # Check password (converting strings back to bytes for bcrypt)
    if not bcrypt.checkpw(body.password.encode("utf-8"), existing_user.hashed_password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid password")

    # Generate JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": existing_user.username}, 
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}