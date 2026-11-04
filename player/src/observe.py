"""Capture page observation for the learning agent: screenshot + interactive DOM."""

from __future__ import annotations

import base64
from typing import Any

from playwright.sync_api import Page


def screenshot_b64(page: Page) -> str:
    raw = page.screenshot(full_page=False, type="png")
    return base64.b64encode(raw).decode("ascii")


def interactive_elements(page: Page, *, limit: int = 40) -> list[dict[str, Any]]:
    """Return visible clickable-ish elements with selectors the agent can reuse."""
    return page.evaluate(
        """(limit) => {
          const out = [];
          const nodes = Array.from(document.querySelectorAll(
            'button, [role="button"], a, input, select, textarea, [onclick], [data-action], [data-testid]'
          ));
          const seen = new Set();
          for (const el of nodes) {
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            if (rect.width < 2 || rect.height < 2) continue;
            if (style.visibility === 'hidden' || style.display === 'none' || style.opacity === '0') continue;
            const text = (el.innerText || el.value || el.getAttribute('aria-label') || '').trim().slice(0, 80);
            let selector = null;
            if (el.id) selector = `#${CSS.escape(el.id)}`;
            else if (el.getAttribute('data-testid')) selector = `[data-testid="${el.getAttribute('data-testid')}"]`;
            else if (el.getAttribute('data-action')) selector = `[data-action="${el.getAttribute('data-action')}"]`;
            else if (el.getAttribute('aria-label')) selector = `[aria-label="${el.getAttribute('aria-label')}"]`;
            else if (el.tagName === 'BUTTON' && text) selector = `button:has-text("${text.slice(0, 40)}")`;
            else {
              const name = (el.className || '').toString().trim().split(/\\s+/).slice(0, 2).join('.');
              selector = name ? `${el.tagName.toLowerCase()}.${name}` : el.tagName.toLowerCase();
            }
            const key = selector + '|' + text;
            if (seen.has(key)) continue;
            seen.add(key);
            out.push({
              tag: el.tagName.toLowerCase(),
              text,
              selector,
              disabled: !!el.disabled,
              x: Math.round(rect.x + rect.width / 2),
              y: Math.round(rect.y + rect.height / 2),
            });
            if (out.length >= limit) break;
          }
          return out;
        }""",
        limit,
    )


def page_observation(page: Page) -> dict[str, Any]:
    return {
        "url": page.url,
        "title": page.title(),
        "elements": interactive_elements(page),
        "screenshot_b64": screenshot_b64(page),
    }
