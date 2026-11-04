FROM mcr.microsoft.com/playwright/python:v1.49.1-jammy

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fixtures/ /app/fixtures/
COPY src/ /app/src/

RUN mkdir -p /data/policies /data/recordings /data/events

VOLUME ["/data"]

# Default: learn the mock game, then record gameplay video
CMD ["python", "-m", "main", "run", "--game", "mock-slot", "--max-spins", "10"]
