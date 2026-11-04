"""Shared filesystem paths inside the player container."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
POLICIES = Path("/data/policies")
RECORDINGS = Path("/data/recordings")
EVENTS = Path("/data/events")
KNOWLEDGE = Path("/data/knowledge")


def ensure_data_dirs() -> None:
    for path in (POLICIES, RECORDINGS, EVENTS, KNOWLEDGE):
        path.mkdir(parents=True, exist_ok=True)
