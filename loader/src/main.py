"""Blue Wave loader — collect providers and games (with release dates) into db."""

from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Any

from collectors.seed import collect_seed_catalog
from db import catalog_stats, connect, upsert_game, upsert_provider


def wait_for_db(retries: int = 30, delay_sec: float = 2.0) -> None:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with connect() as conn:
                conn.execute("SELECT 1")
            print(f"db ready (attempt {attempt})")
            return
        except Exception as exc:  # noqa: BLE001 — retry until timeout
            last_error = exc
            print(f"waiting for db ({attempt}/{retries}): {exc}")
            time.sleep(delay_sec)
    raise RuntimeError(f"database not reachable after {retries} attempts") from last_error


def load_catalog(providers: list[dict[str, Any]]) -> dict[str, int]:
    provider_count = 0
    game_count = 0

    with connect() as conn:
        with conn.transaction():
            for provider in providers:
                games = provider.pop("games", [])
                provider_id = upsert_provider(conn, provider)
                provider_count += 1
                for game in games:
                    game["provider_id"] = provider_id
                    game["metadata"] = json.dumps(game.get("metadata") or {})
                    upsert_game(conn, game)
                    game_count += 1
        stats = catalog_stats(conn)

    return {
        "upserted_providers": provider_count,
        "upserted_games": game_count,
        "active_providers": int(stats["providers"]),
        "active_games": int(stats["games"]),
        "games_with_release_date": int(stats["games_with_release_date"]),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load Blue Wave providers and games into Postgres")
    parser.add_argument(
        "--collector",
        choices=["seed"],
        default="seed",
        help="Collector to run (seed for now; live sources come later)",
    )
    parser.add_argument(
        "--skip-wait",
        action="store_true",
        help="Do not retry waiting for the database",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.skip_wait:
        wait_for_db()

    if args.collector == "seed":
        providers = collect_seed_catalog()
    else:
        raise ValueError(f"unknown collector: {args.collector}")

    result = load_catalog(providers)
    print(json.dumps({"ok": True, "collector": args.collector, **result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
