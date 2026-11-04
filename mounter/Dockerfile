FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

COPY src/ /app/src/

RUN mkdir -p /data/recordings /data/events /data/mounted

VOLUME ["/data"]

CMD ["python", "-m", "main", "--game", "mock-slot"]
