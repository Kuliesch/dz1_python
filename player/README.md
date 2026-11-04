# player

Контейнер Blue Wave: **йому передають гру**, він відкриває браузер і **за багато ітерацій вчиться в неї грати** за допомогою моделі (API key).

## Ідея

1. Ззовні передається гра: `--game <slug>` + `--url <demo>` (або `GAME_URL`).
2. Контейнер відкриває Chromium (Playwright).
3. Vision/chat-модель (OpenAI-compatible) багато разів:
   - дивиться скріншот + інтерактивний DOM;
   - клікає / чекає / нотує;
   - досліджує інтерфейс, фічі, контролі (spin, bet, info, autoplay…).
4. Зберігає:
   - `/data/knowledge/<game>.json` — журнал дослідження;
   - `/data/policies/<game>.json` — політика для подальшого запису.
5. `record` відтворює політику і пише відео для `mounter`.

API-ключ **не комітиться** — лише env.

## Env

| Змінна | Опис |
| --- | --- |
| `PLAYER_API_KEY` | API ключ моделі (обов’язково для `--mode model`) |
| `PLAYER_API_BASE` | База OpenAI-compatible API (default `https://api.openai.com/v1`) |
| `PLAYER_MODEL` | Модель (default `gpt-4o-mini`) |
| `GAME_URL` | Demo URL гри |
| `PLAYER_LEARN_ITERATIONS` | Кількість ітерацій навчання (default 25) |

## Запуск

```bash
export PLAYER_API_KEY=sk-...
export GAME_URL="https://example.com/demo"

docker compose --profile play run --rm \
  -e PLAYER_API_KEY \
  -e PLAYER_API_BASE \
  -e PLAYER_MODEL \
  -e GAME_URL \
  player \
  python -m main learn --game sweet-bonanza --url "$GAME_URL" --iterations 30

docker compose --profile play run --rm \
  -e GAME_URL \
  player \
  python -m main record --game sweet-bonanza --max-spins 20
```

Без ключа `--mode auto` падає назад на heuristic (лише для mock fixture / простих DOM).

## Режими learn

| `--mode` | Поведінка |
| --- | --- |
| `auto` | model якщо є `PLAYER_API_KEY`, інакше heuristic |
| `model` | тільки модель (потрібен ключ) |
| `heuristic` | швидкий DOM fallback без моделі |
