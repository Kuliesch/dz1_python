"""Playwright browser session helpers."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from playwright.sync_api import Browser, Page, Playwright, sync_playwright


@contextmanager
def browser_page(
    *,
    headless: bool = True,
    record_dir: Path | None = None,
    viewport: tuple[int, int] = (1280, 720),
) -> Iterator[tuple[Playwright, Browser, Page]]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        context_kwargs: dict = {
            "viewport": {"width": viewport[0], "height": viewport[1]},
        }
        if record_dir is not None:
            record_dir.mkdir(parents=True, exist_ok=True)
            context_kwargs["record_video_dir"] = str(record_dir)
            context_kwargs["record_video_size"] = {
                "width": viewport[0],
                "height": viewport[1],
            }
        context = browser.new_context(**context_kwargs)
        page = context.new_page()
        try:
            yield playwright, browser, page
        finally:
            context.close()
            browser.close()
