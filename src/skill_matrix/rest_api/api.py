from fastapi import FastAPI

from src.skill_matrix.database import engine
from src.skill_matrix.models import Base
from src.skill_matrix.rest_api import auth, skills, projects

app = FastAPI(
    title="SkillMatrix Connect API",
    version="1.0",
    description="REST API для управления компетенциями",
)

#Cоздать таблицы
Base.metadata.create_all(engine)

#Подключить роутеры
app.include_router(auth.router)
app.include_router(skills.router)
app.include_router(projects.router)



@app.get("/")
def root():
    return {"message": "SkillMatrix Connect API"}