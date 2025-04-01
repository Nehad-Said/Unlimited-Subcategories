# Stage 1: Builder
FROM python:3.10-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.7.1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry==$POETRY_VERSION

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Stage 2: Runtime
FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -U -d /app appuser && \
    mkdir /app && \
    chown appuser:appuser /app

# Copy installed Python packages
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app
COPY --chown=appuser . .

USER appuser

# Verify Django is installed
RUN python -c "import django; print(django.__version__)"

CMD ["gunicorn", "category_project.wsgi:application", "--bind", "0.0.0.0:8000"]
