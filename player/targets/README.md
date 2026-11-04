# Player targets

| Slug | Mode | URL / fixture | Статус |
| --- | --- | --- | --- |
| `lucky-baker` | **mock (default now)** | `fixtures/lucky_baker_mock.html` | Offline learn — option 3 |
| `lucky-baker` | live | https://stake.com/casino/games/jeellee-lucky-baker | Blocked by Cloudflare from agent network |

## Mock learn (рекомендовано зараз)

```bash
export PLAYER_API_KEY=...
set -a && source .env && source player/targets/lucky-baker-mock.env && set +a
export DATA_ROOT=./.data PYTHONPATH=player/src

python3 -m main learn --game "$GAME_SLUG" --url "$GAME_URL" --mode model --iterations 15
python3 -m main record --game "$GAME_SLUG" --url "$GAME_URL" --max-spins 12
```

Або через compose:

```bash
PLAYER_USE_MOCK=1 GAME_URL=mock://lucky-baker \
  docker compose --profile play run --rm player \
  python -m main learn --game lucky-baker --url mock://lucky-baker --mode model --iterations 15
```

## Live Stake (коли буде доступна мережа/браузер)

```bash
set -a && source player/targets/lucky-baker.env && set +a
# PLAYER_USE_MOCK must be unset
docker compose --profile play run --rm player \
  python -m main learn --game "$GAME_SLUG" --url "$GAME_URL" --mode model --iterations 30
```
