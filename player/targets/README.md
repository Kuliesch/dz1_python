# Player targets

Список ігор, які передаються в контейнер `player`.

| Slug | URL | Статус |
| --- | --- | --- |
| `lucky-baker` | https://stake.com/casino/games/jeellee-lucky-baker | Перша ціль (пілот) |

## Запуск навчання

```bash
export PLAYER_API_KEY=...          # обов'язково для model mode
export PLAYER_API_BASE=https://api.openai.com/v1
export PLAYER_MODEL=gpt-4o-mini

set -a && source player/targets/lucky-baker.env && set +a

docker compose --profile play run --rm player \
  python -m main learn \
    --game "$GAME_SLUG" \
    --url "$GAME_URL" \
    --mode model \
    --iterations "${PLAYER_LEARN_ITERATIONS:-30}"
```

## Відомі обмеження (Lucky Baker @ Stake)

- Сторінка може вимагати акаунт / geo / age-gate — model agent клікає лише явні demo/accept контроли.
- Datacenter IP часто отримує **403** від Stake (WAF) — для реального прогону потрібен доступний мережевий шлях (локальний браузер / residential / VPN у дозволеній юрисдикції).
- Не автоматизуємо депозити / real-money cashier.
- RTP і точну дату релізу треба фактчекнути з провайдера перед публікацією огляду.
