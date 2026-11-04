# player

Контейнер Blue Wave: **спочатку навчитись грати**, потім відкрити браузер, зіграти демосесію і **записати відео**.

## Фази

| Команда | Що робить |
| --- | --- |
| `learn` | Відкриває гру, шукає кнопку spin, міряє темп, зберігає policy в `/data/policies/` |
| `record` | Завантажує policy, грає N спінів, пише `/data/recordings/<game>.webm` + event log |
| `run` | `learn` → `record` підряд (entrypoint за замовчуванням) |

За замовчуванням використовується локальний fixture `fixtures/mock_slot.html` (без real-money). Для дозволеного демо: `--url https://…`.

## Запуск

```bash
docker compose --profile play run --rm player
# або окремо:
docker compose --profile play run --rm player python -m main learn --game mock-slot
docker compose --profile play run --rm player python -m main record --game mock-slot --max-spins 15
```

Вихід (volume `media_data`):

- `/data/policies/<game>.json` — навчена політика
- `/data/recordings/<game>.webm` — відео для `mounter`
- `/data/events/<game>.json` — лог спінів/подій
