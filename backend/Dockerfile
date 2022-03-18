FROM python:3.9.7-slim AS builder

WORKDIR /opt/poc-neo4j/backend

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt > requirements.txt


FROM python:3.9.7-slim

ENV POETRY_VERSION=1.1.13
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/poc-neo4j/backend

COPY --from=builder /opt/poc-neo4j/backend/requirements.txt .

RUN pip install "poetry==$POETRY_VERSION"

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0" ]
