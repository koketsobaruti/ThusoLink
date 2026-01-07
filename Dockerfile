# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock from backend for caching
COPY pyproject.toml /app/pyproject.toml
COPY src/backend/poetry.lock /app/poetry.lock

# Install pip and Poetry
RUN pip install --upgrade pip && pip install poetry

# Install dependencies without installing the project itself
# RUN poetry install --no-root
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy the rest of the src folder
COPY src /app/src

# Set working directory to src
WORKDIR /app/src

# Expose port 8000
EXPOSE 8000

# Run Alembic migrations and then start the app
CMD ["sh", "-c", "alembic upgrade head && uvicorn app:app --host 0.0.0.0 --port 8000"]
