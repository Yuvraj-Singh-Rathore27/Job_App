from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .schema import RegisterSchema, LoginSchema  # Relative import
from .crud import create_user, get_user_by_email, verify_password  # Relative import
from app.db import SessionLocal
from app.utils.response import success_response, error_response
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_user(data: RegisterSchema, db: Session = Depends(get_db)):
    if get_user_by_email(db, data.email):
        return error_response("Email already exists")

    user = create_user(db, data.name, data.email, data.password)

    return success_response({
        "message": "User registered successfully",
        "user": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email
        }
    })


@router.post("/login")
def login_user(data: LoginSchema, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.password_hash):
        return error_response("Invalid email or password")

    token = create_access_token({"user_id": str(user.id)})

    return success_response({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email
        }
    })
    

