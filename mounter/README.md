# mounter

Контейнер Blue Wave: **монтаж** сирого запису з `player` у короткий review-ролик.

## Вхід → вихід

| Вхід | Вихід |
| --- | --- |
| `/data/recordings/<game>.webm` | `/data/mounted/<game>_review.mp4` |
| `/data/events/<game>.json` (опційно) | title / spins у burn-in |

Пайплайн (ffmpeg): scale 1280×720 → trim до ~2.5 хв → title/subtitle/disclaimer overlay → H.264 MP4.

Disclaimer на екрані: *Selected episodes · not typical outcome frequency* (згідно з концептом).

## Запуск

Спочатку потрібен запис player (той самий volume `player_data`):

```bash
docker compose --profile play run --rm player
docker compose --profile mount run --rm mounter
```

Опції:

```bash
docker compose --profile mount run --rm mounter \
  python -m main --game mock-slot --title "Mock Slot" --max-seconds 120
```
