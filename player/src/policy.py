"""Learned play policy — what to click and how to pace spins."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class PlayPolicy:
    game_slug: str
    start_url: str
    spin_selector: str
    busy_indicator: str | None = None
    spin_delay_ms: int = 1200
    post_spin_wait_ms: int = 900
    max_spins: int = 20
    learned_from: str = "heuristic"
    notes: list[str] = field(default_factory=list)
    extras: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def save(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    @classmethod
    def load(cls, path: Path) -> "PlayPolicy":
        data = json.loads(path.read_text(encoding="utf-8"))
        known = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})
