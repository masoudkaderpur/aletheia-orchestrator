FROM python:3.12-slim AS builder

RUN pip install poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --without dev

FROM python:3.12-slim AS runtime

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src/

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "src/aletheia_orchestrator/main.py"]
