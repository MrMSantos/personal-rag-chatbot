FROM python:3.11 AS rag-backend

ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends

RUN pip install --upgrade --no-cache-dir -U pip uv

COPY pyproject.toml uv.lock ./

RUN uv sync --no-cache

COPY ./rag/api /app/rag/api
COPY ./rag/backend /app/rag/backend

EXPOSE 5432
EXPOSE 8000

CMD ["uv", "run", "uvicorn", "rag.api.v1.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug", "--reload"]
