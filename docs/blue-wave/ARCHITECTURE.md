# Blue Wave — технічна структура (v0.1 sketch)

## Контейнери

Кожна папка = окремий контейнер.

| Папка | Роль |
| --- | --- |
| `db/` | Postgres. Каталог провайдерів і ігор у **окремих таблицях**. |
| `loader/` | Збір провайдерів + ігор з **датами релізів** → upsert у `db`. |
| `player/` | Передається гра → модель за багато ітерацій досліджує UI/фічі й вчиться грати → запис відео. |
| `mounter/` | Монтаж сирого запису → короткий review MP4. |
| `admin-api/` | HTTP API для адмінки (каталог + media status). |
| `admin/` | Веб-адмінка (nginx SPA → проксі на admin-api). |

## Player (детальніше)

Вхід:

- `--game <slug>` — ідентифікатор
- `--url` / `GAME_URL` / `mock://lucky-baker` — URL або локальний fixture
- `PLAYER_USE_MOCK=1` — offline fixture (поточний пілот)
- `PLAYER_API_KEY` (+ опційно `PLAYER_API_BASE`, `PLAYER_MODEL`)

Цикл `learn` (mode=model):

1. Відкрити браузер (Playwright/Chromium).
2. На кожній ітерації: скріншот + список інтерактивних елементів → модель.
3. Модель повертає JSON-дію: `click` / `wait` / `note` / `done` + discovery (controls, features, ui_regions).
4. Агент виконує дію, накопичує knowledge.
5. Коли знайдено `spin` (і модель каже ready) → зберегти policy.

**Пілот зараз:** Lucky Baker mock (`player/fixtures/lucky_baker_mock.html`), бо live Stake блокується Cloudflare з agent-мережі.

Артефакти (`media_data` / локально `.data/`):

| Шлях | Зміст |
| --- | --- |
| `…/knowledge/<game>.json` | журнал ітерацій, фічі, контролі |
| `…/policies/<game>.json` | політика для record |
| `…/recordings/<game>.webm` | сирий геймплей |
| `…/events/<game>.json` | лог спінів |
| `…/mounted/<game>_review.mp4` | монтаж від mounter |

```bash
export PLAYER_API_KEY=...
export PLAYER_USE_MOCK=1 GAME_URL=mock://lucky-baker

python3 -m main learn --game lucky-baker --url mock://lucky-baker --mode model --iterations 15
```

## Запуск стеку

```bash
docker compose up -d --build db admin-api admin
docker compose --profile load run --rm loader
docker compose --profile play run --rm player
docker compose --profile mount run --rm mounter
```

## Схема даних

```
providers 1───* games
```

## Пайплайн

```
loader → db
player (model learn → record) → mounter → mounted MP4
admin ← admin-api ← db + media volume
```
