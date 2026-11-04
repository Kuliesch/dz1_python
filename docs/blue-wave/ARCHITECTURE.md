# Blue Wave — технічна структура (v0.1 sketch)

## Контейнери

Кожна папка = окремий контейнер.

| Папка | Роль |
| --- | --- |
| `db/` | Postgres. Каталог провайдерів і ігор у **окремих таблицях**. |
| `loader/` | Збір провайдерів + ігор з **датами релізів** → upsert у `db`. |
| `player/` | Браузер → **спочатку learn**, потім грає демо і **записує відео**. |
| `mounter/` | Монтаж сирого запису → короткий review MP4. |
| `admin-api/` | HTTP API для адмінки (каталог + media status). |
| `admin/` | Веб-адмінка (nginx SPA → проксі на admin-api). |

## Запуск

```bash
# ядро: db + admin stack
docker compose up -d --build db admin-api admin
# UI: http://localhost:8080
# API: http://localhost:8000/health

# каталог
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

`admin-api` монтує той самий volume (read) для `/api/media`.

## Схема даних

```
providers 1───* games
```

## Пайплайн

```
loader → db
player (learn→record) → mounter → mounted MP4
admin ← admin-api ← db + media volume
```
