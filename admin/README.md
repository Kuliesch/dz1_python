# admin

Веб-адмінка Blue Wave (окремий контейнер на nginx).

UI читає дані через `/api/*`, які проксіюються на `admin-api`.

## Запуск

```bash
docker compose up -d --build db admin-api admin
# відкрити http://localhost:8080
```

Розділи: Overview · Providers · Games · Media.
