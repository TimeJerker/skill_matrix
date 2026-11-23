from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DATABASE_PASS: str = "135Aaa"
    DB_NAME: str = "skill_matrix"

    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASS: str = "guest"

    GRPC_HOST: str = "localhost"
    GRPC_PORT: int = 50051

    WS_HOST: str = "0.0.0.0"  # внутри контейнера слушаем на всех интерфейсах
    WS_PORT: int = 8001

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8")

    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DATABASE_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    def RABBITMQ_URL(self) -> str:
        return (
            f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"
        )

    def GRPC_ADDRESS(self) -> str:
        return f"{self.GRPC_HOST}:{self.GRPC_PORT}"


settings = Settings()
