# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock /code/

RUN poetry install --no-root --no-dev

COPY . /code/

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "server_main.main:app", "--host", "0.0.0.0", "--port", "8000"]

