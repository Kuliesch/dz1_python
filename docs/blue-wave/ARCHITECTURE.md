# Blue Wave — технічна структура (v0.1 sketch)

## Контейнери

| Папка | Роль |
| --- | --- |
| `db/` | Postgres-контейнер. Каталог провайдерів і ігор у **окремих таблицях**. |
| `loader/` | Контейнер збору: провайдери + ігри з **датами релізів** → upsert у `db`. |

Запуск:

```bash
docker compose up -d --build db
docker compose --profile load run --rm loader
```

## Схема даних

```
providers 1───* games
```

- `providers` — slug, name, website, country, source/collected_at
- `games` — provider_id, slug, name, **release_date**, rtp, volatility, demo_url, metadata JSONB

Унікальність: `providers.slug`; `(games.provider_id, games.slug)`.

## Loader

Зараз: collector `seed` читає `loader/data/seed_catalog.json` (демо-каталог для перевірки пайплайну).

Далі: окремі collectors під живі джерела (API/скрапінг за наявності прав), без зміни схеми таблиць.

## Наступні блоки (з обговорення)

- `player/` — контейнер: браузер → грає в демо → запис відео (спочатку навчання грі)
- AI Video Studio / сайт — після даних і запису геймплею
