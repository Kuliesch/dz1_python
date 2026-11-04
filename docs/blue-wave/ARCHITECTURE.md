# Blue Wave — технічна структура (v0.1 sketch)

## Контейнери

Кожна папка = окремий контейнер.

| Папка | Роль |
| --- | --- |
| `db/` | Postgres. Каталог провайдерів і ігор у **окремих таблицях**. |
| `loader/` | Збір провайдерів + ігор з **датами релізів** → upsert у `db`. |
| `player/` | Браузер → **спочатку learn**, потім грає демо і **записує відео** (+ event log). |
| `mounter/` | *(далі)* монтаж відео з записів player. |
| `admin-api/` / `admin/` | *(далі)* API та веб-адмінка. |

## Запуск

```bash
# каталог
docker compose up -d --build db
docker compose --profile load run --rm loader

# геймплей: learn → record
docker compose --profile play run --rm player
```

Артефакти player (volume `player_data`):

- `/data/policies/<game>.json`
- `/data/recordings/<game>.webm` ← вхід для mounter
- `/data/events/<game>.json`

## Схема даних

```
providers 1───* games
```

- `providers` — slug, name, website, country, source/collected_at
- `games` — provider_id, slug, name, **release_date**, rtp, volatility, demo_url, metadata JSONB

## Player: learn → record

1. **learn** — відкрити URL (fixture або дозволене демо), знайти spin-контроль, виміряти темп, зберегти policy.
2. **record** — відтворити policy на N спінів, записати Playwright video + події.
3. Без навченої policy запис не стартує (явний fail).

За замовчуванням — `player/fixtures/mock_slot.html` для офлайн-прогону пайплайну.
