from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.skill_matrix.database import get_db
from src.skill_matrix import crud
from src.skill_matrix.rest_api.schemas import UserRegister, UserLogin, UserResponse

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

    user = crud.create_user(
        db,
        username=data.username,
        email=data.email,
        password=data.password,
        role_id=data.role_id,
        department=data.department,
    )
    return user


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Вход пользователя"""
    user = crud.read_user_by_username(db, data.username)
    if not user or user.password != data.password:
        raise HTTPException(401, "Неверный логин или пароль")
    return {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "role_id": user.role_id,
    }