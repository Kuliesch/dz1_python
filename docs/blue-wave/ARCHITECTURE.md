# Blue Wave — технічна структура (v0.1 sketch)

## Контейнери

Кожна папка = окремий контейнер.

| Папка | Роль |
| --- | --- |
| `db/` | Postgres. Каталог провайдерів і ігор у **окремих таблицях**. |
| `loader/` | Збір провайдерів + ігор з **датами релізів** → upsert у `db`. |
| `player/` | Браузер → **спочатку learn**, потім грає демо і **записує відео**. |
| `mounter/` | Монтаж сирого запису → короткий review MP4 (title + disclaimer). |
| `admin-api/` / `admin/` | *(далі)* API та веб-адмінка. |

## Запуск

```bash
# каталог
docker compose up -d --build db
docker compose --profile load run --rm loader

# геймплей + монтаж (спільний volume media_data)
docker compose --profile play run --rm player
docker compose --profile mount run --rm mounter
```

### Media volume (`media_data` → `/data`)

| Шлях | Хто пише | Зміст |
| --- | --- | --- |
| `/data/policies/` | player | навчені play policies |
| `/data/recordings/<game>.webm` | player | сирий геймплей |
| `/data/events/<game>.json` | player | лог спінів |
| `/data/mounted/<game>_review.mp4` | mounter | змонтований огляд |

## Схема даних

```
providers 1───* games
```

- `providers` — slug, name, website, country, source/collected_at
- `games` — provider_id, slug, name, **release_date**, rtp, volatility, demo_url, metadata JSONB

## Пайплайн відео

```
player (learn → record) → mounter (trim/overlay) → /data/mounted/*_review.mp4
```

1. **learn** — знайти spin-контроль, виміряти темп, зберегти policy.
2. **record** — зіграти N спінів, webm + events.
3. **mount** — trim ~2–3 хв, burn-in title, disclaimer *Selected episodes*.
