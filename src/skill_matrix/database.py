from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from src.skill_matrix.config import settings
from src.skill_matrix.models import Base, Role

engine = create_engine(settings.DATABASE_URL(), echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def create_tables():
    Base.metadata.create_all(engine)
    print("Таблицы созданы")