from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.skill_matrix.rest_api import schemas
from src.skill_matrix import crud
from src.skill_matrix.database import get_db

router = APIRouter(
    prefix="/skill",
    tags=["Skills"]
)

@router.post("/", response_model=schemas.SkillResponse)
def create_skill_endpoint(skill: schemas.SkillCreate, db: Session = Depends(get_db)):

    if crud.read_skill_by_name(db, name=skill.name):
        raise HTTPException(status_code=402, detail="Skill already exists")
    
    return crud.create_skill(session=db, name=skill.name, category=skill.category)

@router.get("/", response_model=List[schemas.SkillResponse])
def get_all_skills_endpoint(db: Session = Depends(get_db)):
    return crud.read_all_skills(db)

@router.get("/{skill_id}", response_model=schemas.SkillResponse)
def get_skill_endpoint(skill_id: int, db: Session = Depends(get_db)):
    skill = crud.read_skill(db, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.patch("/{skill_id}", response_model=schemas.SkillResponse)
def update_skill_endpoint(skill_id: int, skill_data: schemas.SkillUpdate, db: Session = Depends(get_db)):
    updated_skill = crud.update_skill(db, skill_id, name=skill_data.name, category=skill_data.category)
    if not updated_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return updated_skill

@router.delete("/{skill_id}")
def delete_skill_endpoint(skill_id: int, db: Session = Depends(get_db)):
    success = crud.delete_skill(db, skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"message": "Skill successfully deleted"}