# app/routers/projects.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.skill_matrix.rest_api import schemas
from src.skill_matrix import crud
from src.skill_matrix.database import get_db

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=schemas.ProjectResponse)
def create_project_endpoint(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(
        session=db, 
        title=project.title, 
        description=project.description, 
        manager_id=project.manager_id
    )

@router.get("/", response_model=List[schemas.ProjectResponse])
def get_all_projects_endpoint(db: Session = Depends(get_db)):
    return crud.read_all_projects(db)

@router.get("/{project_id}", response_model=schemas.ProjectResponse)
def get_project_endpoint(project_id: int, db: Session = Depends(get_db)):
    project = crud.read_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.patch("/{project_id}", response_model=schemas.ProjectResponse)
def update_project_endpoint(project_id: int, project_data: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    updated_project = crud.update_project(
        db, 
        project_id, 
        title=project_data.title, 
        description=project_data.description
    )
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

@router.delete("/{project_id}")
def delete_project_endpoint(project_id: int, db: Session = Depends(get_db)):
    success = crud.delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project successfully deleted"}