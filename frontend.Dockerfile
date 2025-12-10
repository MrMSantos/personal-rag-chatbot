FROM python:3.11 AS rag-frontend

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends

RUN pip install --upgrade --no-cache-dir -U pip uv

COPY pyproject.toml uv.lock ./

RUN uv sync --no-cache

COPY ./rag/frontend /app/rag/frontend

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "rag/frontend/Home.py"]
