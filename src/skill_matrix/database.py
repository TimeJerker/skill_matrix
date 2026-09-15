import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

db_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=os.getenv("DATABASE_PASSWORD"),
    host="localhost",
    port=5432,
    database="skill_matrix",
)

engine = create_engine(db_url, echo=True, client_encoding='utf8')

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            print("Успешное подключение")
            print("Версия сервера:", result.fetchone()[0])
    except Exception as e:
        print("Ошибка подключения: ")
        print(e)