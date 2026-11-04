# Blue Wave

Video-first мережа AI-оглядів слотів з власним каталогом ігор.

## Структура

| Шлях | Призначення |
| --- | --- |
| `db/` | Postgres-контейнер: таблиці `providers` і `games` |
| `loader/` | Контейнер збору провайдерів/ігор з датами релізів |
| `docs/blue-wave/` | Концепт, Stage 0 Kick feasibility, архітектура |

## Швидкий старт (каталог)

```bash
docker compose up -d --build db
docker compose --profile load run --rm loader
```

Перевірка:

```bash
docker compose exec db psql -U bluewave -d bluewave -c \
  "SELECT p.name, g.name, g.release_date FROM games g JOIN providers p ON p.id = g.provider_id ORDER BY g.release_date DESC NULLS LAST;"
```

## Документація

- [`docs/blue-wave/CONCEPT.md`](docs/blue-wave/CONCEPT.md) — продуктова концепція v0.1
- [`docs/blue-wave/STAGE0_KICK_FEASIBILITY.md`](docs/blue-wave/STAGE0_KICK_FEASIBILITY.md) — Kick GO/NO-GO
- [`docs/blue-wave/ARCHITECTURE.md`](docs/blue-wave/ARCHITECTURE.md) — технічна структура
