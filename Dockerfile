# Builder stage
FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION=1.5.1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

# Use poetry to install dependencies
RUN poetry export -f requirements.txt --without-hashes --output /app/requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r /app/requirements.txt

# Final stage
FROM python:3.11-slim AS final

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r /tmp/requirements.txt \
    && rm -rf /wheels /tmp/requirements.txt

# Cleanup and setup app user and directory
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -U liara \
    && install -d -m 0755 -o liara -g liara /app/staticfiles

WORKDIR /app

COPY --chown=liara:liara . .

USER liara:liara

RUN chmod +x ./entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]
CMD [ "server" ]
