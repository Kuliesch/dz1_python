"""Seed collector — loads providers/games from a local JSON catalog."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_SEED_PATH = Path(__file__).resolve().parents[2] / "data" / "seed_catalog.json"


def collect_seed_catalog(path: Path | None = None) -> list[dict[str, Any]]:
    seed_path = path or DEFAULT_SEED_PATH
    with seed_path.open(encoding="utf-8") as handle:
        payload = json.load(handle)

    source = payload.get("source", "seed")
    providers: list[dict[str, Any]] = []
    for item in payload.get("providers", []):
        providers.append(
            {
                "slug": item["slug"],
                "name": item["name"],
                "website_url": item.get("website_url"),
                "country_code": item.get("country_code"),
                "source": source,
                "source_ref": str(seed_path.name),
                "games": [
                    {
                        "slug": game["slug"],
                        "name": game["name"],
                        "release_date": game.get("release_date"),
                        "game_type": game.get("game_type", "slot"),
                        "rtp_percent": game.get("rtp_percent"),
                        "volatility": game.get("volatility"),
                        "demo_url": game.get("demo_url"),
                        "thumbnail_url": game.get("thumbnail_url"),
                        "source": source,
                        "source_ref": str(seed_path.name),
                        "metadata": game.get("metadata") or {},
                    }
                    for game in item.get("games", [])
                ],
            }
        )
    return providers
