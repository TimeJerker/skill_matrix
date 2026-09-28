from sqlalchemy import create_engine, insert
from config import settings
from models import Base, Role

engine = create_engine(settings.DATABASE_URL())

def create_tables():
    with engine.connect() as conn:
        Base.metadata.create_all(conn)
        conn.commit()

def insert_data():
    with engine.connect() as conn:
        stmt = insert(Role).values(name="Admin")
        conn.execute(stmt)
        conn.commit()
