# STAGE 1: Build Environment
# Using a 'slim' base image to maintain a low footprint while
# providing the necessary C-extensions for Python package compilation.
FROM python:3.12-slim AS builder

# Installing Poetry: The project's dependency manager.
RUN pip install poetry

# POETRY CONFIGURATION:
# 1. NO_INTERACTION: Ensures the build doesn't hang waiting for user input.
# 2. IN_PROJECT: Forces the virtual environment to be created within /app/.venv.
# 3. CREATE: Ensures a clean environment is generated during the build.
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

WORKDIR /app

# Dependency Resolution:
# Only the lock-files are copied first to leverage Docker's layer caching.
# If pyproject.toml hasn't changed, Docker skips the expensive install step.
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --without dev

# STAGE 2: Runtime Environment
# A fresh, clean image that will only contain the essentials for execution.
FROM python:3.12-slim AS runtime

WORKDIR /app

# Resource Transfer:
# Only the pre-compiled virtual environment is copied from the builder.
# This leaves behind the Poetry tool and the cache, saving hundreds of megabytes.
COPY --from=builder /app/.venv /app/.venv

# Application Code:
# The source logic is copied into the runtime stage.
COPY src/ /app/src/

# Path Configuration:
# Adds the virtual environment's binary folder to the system path.
# This allows 'python' to find the installed libraries (LangChain, LangGraph, etc.).
ENV PYTHONPATH="/app/src"
ENV PATH="/app/.venv/bin:$PATH"
# Entry Point:
# Defines the command to execute the orchestrator when the container starts.
CMD ["python", "src/aletheia_orchestrator/main.py"]
