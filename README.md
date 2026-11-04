# Blue Wave

Video-first мережа AI-оглядів слотів з власним каталогом ігор.

## Структура (кожна папка = окремий контейнер)

| Шлях | Призначення |
| --- | --- |
| `db/` | Postgres: `providers` + `games` |
| `loader/` | Збір провайдерів/ігор з датами релізів |
| `player/` | Передається гра → модель вчиться грати (багато ітерацій) → video |
| `mounter/` | Монтаж запису → review MP4 |
| `admin-api/` | HTTP API для адмінки |
| `admin/` | Веб-адмінка |
| `docs/blue-wave/` | Концепт, Stage 0, архітектура |

## Швидкий старт

```bash
# адмінка + db
docker compose up -d --build db admin-api admin
# http://localhost:8080

# наповнити каталог
docker compose --profile load run --rm loader

# геймплей: передати гру + API ключ моделі
export PLAYER_API_KEY=...
export GAME_URL=https://example.com/demo
docker compose --profile play run --rm player \
  python -m main learn --game demo-slot --url "$GAME_URL" --iterations 30
docker compose --profile play run --rm player \
  python -m main record --game demo-slot --max-spins 20
docker compose --profile mount run --rm mounter
```


## Документація

- [`docs/blue-wave/ARCHITECTURE.md`](docs/blue-wave/ARCHITECTURE.md)
- [`docs/blue-wave/CONCEPT.md`](docs/blue-wave/CONCEPT.md)
- [`docs/blue-wave/STAGE0_KICK_FEASIBILITY.md`](docs/blue-wave/STAGE0_KICK_FEASIBILITY.md)
- [`admin-api/README.md`](admin-api/README.md)
- [`admin/README.md`](admin/README.md)
