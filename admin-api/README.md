# admin-api

HTTP API для адмінки Blue Wave (окремий контейнер).

## Ендпоінти

| Method | Path | Опис |
| --- | --- | --- |
| GET | `/health` | Статус API + Postgres |
| GET | `/api/summary` | Лічильники каталогу та media |
| GET | `/api/providers` | Список провайдерів |
| GET | `/api/providers/{slug}` | Провайдер + його ігри |
| GET | `/api/games` | Ігри (`?provider=slug`) |
| GET | `/api/media` | Файли recordings / mounted / policies |

## Запуск

```bash
docker compose up -d --build db admin-api
curl http://localhost:8000/health
```
