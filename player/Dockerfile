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

RUN mkdir -p /data/policies /data/recordings /data/events /data/knowledge

VOLUME ["/data"]

# Pass game via GAME_SLUG/GAME_URL and API key via PLAYER_API_KEY
CMD ["python", "-m", "main", "learn", "--game", "mock-slot", "--mode", "auto", "--iterations", "15"]
