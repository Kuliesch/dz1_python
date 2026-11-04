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

# Default pilot: Lucky Baker local mock (set PLAYER_USE_MOCK=0 + live GAME_URL for Stake)
CMD ["sh", "-c", "python -m main learn --game \"${GAME_SLUG:-lucky-baker}\" --url \"${GAME_URL:-mock://lucky-baker}\" --mode auto --iterations \"${PLAYER_LEARN_ITERATIONS:-15}\""]
