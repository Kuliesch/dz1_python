"""Shared filesystem paths inside the player container."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"

# In Docker default is /data; locally override with DATA_ROOT=./.data
DATA_ROOT = Path(os.environ.get("DATA_ROOT", "/data"))
POLICIES = DATA_ROOT / "policies"
RECORDINGS = DATA_ROOT / "recordings"
EVENTS = DATA_ROOT / "events"
KNOWLEDGE = DATA_ROOT / "knowledge"


def ensure_data_dirs() -> None:
    for path in (POLICIES, RECORDINGS, EVENTS, KNOWLEDGE):
        path.mkdir(parents=True, exist_ok=True)
