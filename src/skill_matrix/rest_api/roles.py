from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.skill_matrix.database import get_db
from src.skill_matrix import crud
from src.skill_matrix.rest_api.schemas import RoleResponse

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return crud.read_all_roles(db)


@router.post("", response_model=RoleResponse, status_code=201)
def create_role(name: str, db: Session = Depends(get_db)):
    return crud.create_role(db, name)


@router.delete("/{role_id}", status_code=204)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    if not crud.delete_role(db, role_id):
        raise HTTPException(404, "Роль не найдена")
    return None