"""Execute a learned policy: play the game and emit gameplay events."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from playwright.sync_api import Page

from policy import PlayPolicy


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def play_with_policy(
    page: Page,
    policy: PlayPolicy,
    *,
    max_spins: int | None = None,
    events_path: Path | None = None,
) -> list[dict[str, Any]]:
    page.goto(policy.start_url, wait_until="domcontentloaded")
    page.wait_for_timeout(500)

    spins = max_spins or policy.max_spins
    button = page.locator(policy.spin_selector).first
    events: list[dict[str, Any]] = []

    for index in range(1, spins + 1):
        button.wait_for(state="visible")
        try:
            if button.is_disabled():
                page.wait_for_timeout(policy.post_spin_wait_ms)
        except Exception:  # noqa: BLE001
            pass

        button.click()
        event: dict[str, Any] = {
            "type": "spin",
            "index": index,
            "at": _now(),
        }
        page.wait_for_timeout(policy.post_spin_wait_ms)

        # Capture mock fixture telemetry when available
        try:
            last = page.evaluate("() => window.__lastSpin || null")
            if last:
                event["result"] = last
        except Exception:  # noqa: BLE001
            pass

        events.append(event)
        page.wait_for_timeout(policy.spin_delay_ms)

    if events_path is not None:
        events_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "game_slug": policy.game_slug,
            "start_url": policy.start_url,
            "recorded_at": _now(),
            "spins": len(events),
            "events": events,
        }
        events_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    return events
