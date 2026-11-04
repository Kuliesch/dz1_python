"""Accumulated knowledge about a game UI while the agent explores."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class GameKnowledge:
    game_slug: str
    start_url: str
    model: str
    controls: dict[str, str] = field(default_factory=dict)
    features: list[str] = field(default_factory=list)
    ui_regions: dict[str, str] = field(default_factory=dict)
    hypotheses: list[str] = field(default_factory=list)
    iteration_log: list[dict[str, Any]] = field(default_factory=list)
    ready_to_play: bool = False
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def touch(self) -> None:
        self.updated_at = _now()

    def merge_discovery(self, discovery: dict[str, Any] | None) -> None:
        if not discovery:
            return
        controls = discovery.get("controls") or {}
        if isinstance(controls, dict):
            for key, value in controls.items():
                if isinstance(key, str) and isinstance(value, str) and value.strip():
                    self.controls[key] = value.strip()
        for feature in discovery.get("features") or []:
            if isinstance(feature, str) and feature and feature not in self.features:
                self.features.append(feature)
        regions = discovery.get("ui_regions") or {}
        if isinstance(regions, dict):
            for key, value in regions.items():
                if isinstance(key, str) and isinstance(value, str) and value.strip():
                    self.ui_regions[key] = value.strip()
        for hypo in discovery.get("hypotheses") or []:
            if isinstance(hypo, str) and hypo and hypo not in self.hypotheses:
                self.hypotheses.append(hypo)
        if discovery.get("ready_to_play") is True:
            self.ready_to_play = True
        self.touch()

    def save(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    @classmethod
    def load(cls, path: Path) -> "GameKnowledge":
        data = json.loads(path.read_text(encoding="utf-8"))
        known = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})
