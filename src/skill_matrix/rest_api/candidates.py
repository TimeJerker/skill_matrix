from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.skill_matrix.database import get_db
from src.skill_matrix import crud
from src.skill_matrix.rest_api.schemas import UserResponse


router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("", response_model=list[UserResponse])
def find_candidates(
    skill_id: int = Query(..., description="ID навыка"),
    project_id: int = Query(..., description="ID проекта"),
    min_level: int = Query(1, description="Минимальный уровень владения"),
    db: Session = Depends(get_db),
):
    """Найти кандидатов для проекта"""
    if not crud.read_skill(db, skill_id):
        raise HTTPException(404, "Навык не найден")

    if not crud.read_project(db, project_id):
        raise HTTPException(404, "Проект не найден")

    candidates = crud.find_candidates_for_project(
        db,
        skill_id=skill_id,
        project_id=project_id,
        min_level=min_level,
    )
    return candidates