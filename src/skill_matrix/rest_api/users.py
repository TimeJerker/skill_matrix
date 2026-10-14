from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.skill_matrix.database import get_db
from src.skill_matrix import crud
from src.skill_matrix.rest_api.schemas import UserResponse, UserRegister, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return crud.read_all_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.read_user(db, user_id)
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    return user


@router.post("", response_model=UserResponse, status_code=201)
def create_user(data: UserRegister, db: Session = Depends(get_db)):
    return crud.create_user(db, data.username, data.email, data.password, data.role_id, data.department)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
):
    user = crud.update_user(
        db,
        user_id,
        username=data.username,
        email=data.email,
        password=data.password,
        role_id=data.role_id,
        department=data.department,
    )
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not crud.delete_user(db, user_id):
        raise HTTPException(404, "Пользователь не найден")
    return None