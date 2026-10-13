from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from src.skill_matrix.database import get_db
from src.skill_matrix import crud
from src.skill_matrix.rest_api.schemas import UserRegister, UserLogin, UserResponse
from src.skill_matrix.rest_api.security import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    if crud.read_user_by_email(db, data.email):
        raise HTTPException(400, "Email уже занят")
    if crud.read_user_by_username(db, data.username):
        raise HTTPException(400, "Username уже занят")
    if not crud.read_role(db, data.role_id):
        raise HTTPException(400, "Роль не найдена")

    hashed_password = get_password_hash(data.password)

    user = crud.create_user(
        db,
        username=data.username,
        email=data.email,
        password=hashed_password,
        role_id=data.role_id,
        department=data.department,
    )
    return user


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Вход пользователя"""
    user = crud.read_user_by_username(db, data.username)
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(401, "Неверный логин или пароль")

    token_data = {"sub": user.username, "user_id": user.user_id}

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }