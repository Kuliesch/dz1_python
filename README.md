# Blue Wave

Video-first мережа AI-оглядів слотів з власним каталогом ігор.

## Структура (кожна папка = контейнер)

| Шлях | Призначення |
| --- | --- |
| `db/` | Postgres: `providers` + `games` |
| `loader/` | Збір провайдерів/ігор з датами релізів |
| `player/` | Learn → play in browser → record video |
| `mounter/` | Монтаж запису → review MP4 |
| `docs/blue-wave/` | Концепт, Stage 0, архітектура |

## Швидкий старт

```bash
# каталог
docker compose up -d --build db
docker compose --profile load run --rm loader

# геймплей + монтаж
docker compose --profile play run --rm player
docker compose --profile mount run --rm mounter
```

Результат монтажу: volume `media_data` → `/data/mounted/<game>_review.mp4`.

## Документація

- [`docs/blue-wave/CONCEPT.md`](docs/blue-wave/CONCEPT.md)
- [`docs/blue-wave/STAGE0_KICK_FEASIBILITY.md`](docs/blue-wave/STAGE0_KICK_FEASIBILITY.md)
- [`docs/blue-wave/ARCHITECTURE.md`](docs/blue-wave/ARCHITECTURE.md)
- [`player/README.md`](player/README.md)
- [`mounter/README.md`](mounter/README.md)
