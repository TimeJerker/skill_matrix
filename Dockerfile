FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-install-project --no-dev

COPY src ./src
COPY main.py ./main.py
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "uvicorn", "src.skill_matrix.rest_api.api:app", "--host", "0.0.0.0", "--port", "8000"]
