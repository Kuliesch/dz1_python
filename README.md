# Blue Wave

Video-first мережа AI-оглядів слотів з власним каталогом ігор.

## Структура (кожна папка = контейнер)

| Шлях | Призначення |
| --- | --- |
| `db/` | Postgres: `providers` + `games` |
| `loader/` | Збір провайдерів/ігор з датами релізів |
| `player/` | Learn → play in browser → record video |
| `docs/blue-wave/` | Концепт, Stage 0, архітектура |

## Швидкий старт

```bash
# 1) каталог
docker compose up -d --build db
docker compose --profile load run --rm loader

# 2) навчитись грати + записати відео (mock slot)
docker compose --profile play run --rm player
```

Окремі фази player:

```bash
docker compose --profile play run --rm player python -m main learn --game mock-slot
docker compose --profile play run --rm player python -m main record --game mock-slot --max-spins 15
```

## Документація

- [`docs/blue-wave/CONCEPT.md`](docs/blue-wave/CONCEPT.md)
- [`docs/blue-wave/STAGE0_KICK_FEASIBILITY.md`](docs/blue-wave/STAGE0_KICK_FEASIBILITY.md)
- [`docs/blue-wave/ARCHITECTURE.md`](docs/blue-wave/ARCHITECTURE.md)
- [`player/README.md`](player/README.md)
