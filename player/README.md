# player

Контейнер Blue Wave: **йому передають гру**, він відкриває браузер і **за багато ітерацій вчиться в неї грати** за допомогою моделі (API key).

## Зараз: mock-first (option 3)

Поки Stake за Cloudflare, пілот **Lucky Baker** вчиться на локальному fixture:

- `fixtures/lucky_baker_mock.html`
- target: `targets/lucky-baker-mock.env` (`GAME_URL=mock://lucky-baker`, `PLAYER_USE_MOCK=1`)

Live URL залишається в `targets/lucky-baker.env` для пізнішого прогону.

## Ідея

1. Передається гра: `--game` + `--url` / `GAME_URL` / `mock://…`
2. Chromium (Playwright)
3. Модель досліджує UI/фічі/контролі ітераціями
4. Пише `/data/knowledge/<game>.json` + `/data/policies/<game>.json`
5. `record` → `/data/recordings/<game>.webm`

## Env

| Змінна | Опис |
| --- | --- |
| `PLAYER_API_KEY` | API ключ моделі |
| `PLAYER_API_BASE` | OpenAI-compatible base |
| `PLAYER_MODEL` | default `gpt-4o-mini` |
| `PLAYER_USE_MOCK` | `1` → локальний fixture |
| `GAME_SLUG` | default `lucky-baker` |
| `GAME_URL` | `mock://lucky-baker` або live URL |

## Запуск (mock)

```bash
export PLAYER_API_KEY=...
set -a && source .env && source player/targets/lucky-baker-mock.env && set +a
export DATA_ROOT=./.data PYTHONPATH=player/src

python3 -m main learn --game "$GAME_SLUG" --url "$GAME_URL" --mode model --iterations 15
python3 -m main record --game "$GAME_SLUG" --url "$GAME_URL" --max-spins 12
```

## Режими learn

| `--mode` | Поведінка |
| --- | --- |
| `auto` | model якщо є ключ, інакше heuristic |
| `model` | тільки модель |
| `heuristic` | DOM fallback без моделі |
