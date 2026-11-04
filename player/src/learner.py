"""Learn how to play a game before recording production footage.

Phase 1 discovers controls and safe spin pacing on a demo/fixture page.
The result is a PlayPolicy used by the record phase.
"""

from __future__ import annotations

import time
from typing import Any

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout

from policy import PlayPolicy

SPIN_CANDIDATES = [
    '[data-testid="spin"]',
    '[data-action="spin"]',
    'button:has-text("SPIN")',
    'button:has-text("Spin")',
    'role=button[name=/spin/i]',
]


def _find_spin_selector(page: Page) -> str:
    for selector in SPIN_CANDIDATES:
        locator = page.locator(selector)
        try:
            if locator.count() > 0 and locator.first.is_visible():
                return selector
        except Exception:  # noqa: BLE001 — try next candidate
            continue
    raise RuntimeError(
        "Could not learn spin control. Extend SPIN_CANDIDATES for this game UI."
    )


def _wait_until_idle(page: Page, selector: str, timeout_ms: int = 8000) -> None:
    try:
        page.wait_for_function(
            """(sel) => {
              if (window.__lastSpin && Date.now() - window.__lastSpin.at < 5000) {
                return true;
              }
              const el = document.querySelector(sel);
              return !!el && !el.disabled;
            }""",
            arg=selector,
            timeout=timeout_ms,
        )
    except PlaywrightTimeout:
        page.wait_for_timeout(1200)


def _measure_spin_cycle(page: Page, selector: str, samples: int = 3) -> tuple[int, int]:
    """Estimate click delay and post-spin settle time from a few practice spins."""
    delays: list[float] = []
    button = page.locator(selector).first

    for _ in range(samples):
        button.wait_for(state="visible")
        _wait_until_idle(page, selector, timeout_ms=3000)
        t0 = time.perf_counter()
        button.click()
        _wait_until_idle(page, selector)
        delays.append((time.perf_counter() - t0) * 1000)
        page.wait_for_timeout(300)

    avg_cycle = int(sum(delays) / len(delays)) if delays else 1500
    spin_delay = max(800, int(avg_cycle * 0.35))
    post_spin = max(600, int(avg_cycle * 0.55))
    return spin_delay, post_spin


def learn_game(
    page: Page,
    *,
    game_slug: str,
    start_url: str,
    practice_spins: int = 3,
) -> PlayPolicy:
    page.goto(start_url, wait_until="domcontentloaded")
    page.wait_for_timeout(500)

    notes: list[str] = []
    spin_selector = _find_spin_selector(page)
    notes.append(f"discovered spin control via {spin_selector}")

    spin_delay_ms, post_spin_wait_ms = _measure_spin_cycle(
        page, spin_selector, samples=max(1, practice_spins)
    )
    notes.append(
        f"measured pacing spin_delay_ms={spin_delay_ms} post_spin_wait_ms={post_spin_wait_ms}"
    )

    extras: dict[str, Any] = {}
    balance = page.locator('[data-testid="balance"]')
    if balance.count():
        extras["balance_selector"] = '[data-testid="balance"]'
        notes.append("tracked balance element")

    return PlayPolicy(
        game_slug=game_slug,
        start_url=start_url,
        spin_selector=spin_selector,
        busy_indicator=None,
        spin_delay_ms=spin_delay_ms,
        post_spin_wait_ms=post_spin_wait_ms,
        learned_from="heuristic-v1",
        notes=notes,
        extras=extras,
    )
