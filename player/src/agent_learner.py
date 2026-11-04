"""Multi-iteration model agent: explore UI/features and learn to play.

The game URL is provided from outside. Over many iterations the model:
  - inspects screenshot + interactive DOM
  - tries actions (click / wait / note)
  - records discovered controls, features, UI regions
  - eventually produces a PlayPolicy for the record phase
"""

from __future__ import annotations

import json
from typing import Any

from playwright.sync_api import Page

from knowledge import GameKnowledge
from model_client import ModelClient
from observe import page_observation
from policy import PlayPolicy

class LearnError(RuntimeError):
    """Learning failed; may still carry partial GameKnowledge for debugging."""

    def __init__(self, message: str, knowledge: GameKnowledge | None = None) -> None:
        super().__init__(message)
        self.knowledge = knowledge


SYSTEM_PROMPT = """You are Blue Wave Player — a careful game-exploration agent.
You receive a browser screenshot and a list of interactive elements for a DEMO slot/casino game UI.
Your job across many iterations: learn how to operate the interface and document features.

Rules:
- Explore only. Prefer safe UI discovery: open menus, paytable/info, settings, then find Spin.
- Never invent RTP, odds, or legal claims. Only describe what you see.
- Never try to deposit, login to real-money cashier, or bypass age gates dishonestly.
- If an age/demo gate is clearly present with an accept control, you may click accept/continue for demo.
- Return ONLY a JSON object (no markdown) with this schema:
{
  "thought": "short reasoning",
  "action": "click" | "wait" | "note" | "done",
  "selector": "playwright/CSS selector when action=click, else null",
  "x": null,
  "y": null,
  "wait_ms": 800,
  "discovery": {
    "controls": {"spin": "...", "plus_bet": "...", "minus_bet": "...", "autoplay": "...", "info": "..."},
    "features": ["free spins", "cascading reels", "..."],
    "ui_regions": {"reels": "...", "hud": "..."},
    "hypotheses": ["spin settles in ~1s", "..."],
    "ready_to_play": false
  }
}
Set action=done and ready_to_play=true only when you know a reliable spin selector and basic pacing.
Prefer selectors from the provided element list.
"""


def _execute_action(page: Page, decision: dict[str, Any]) -> dict[str, Any]:
    action = (decision.get("action") or "wait").lower()
    result: dict[str, Any] = {"action": action, "ok": True}

    if action == "click":
        selector = decision.get("selector")
        if selector:
            try:
                loc = page.locator(str(selector)).first
                loc.wait_for(state="visible", timeout=5000)
                loc.click(timeout=5000)
                result["selector"] = selector
            except Exception as exc:  # noqa: BLE001
                # coordinate fallback if model also provided x/y
                x, y = decision.get("x"), decision.get("y")
                if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                    page.mouse.click(float(x), float(y))
                    result["selector"] = selector
                    result["fallback"] = "coordinates"
                else:
                    result["ok"] = False
                    result["error"] = str(exc)
        else:
            x, y = decision.get("x"), decision.get("y")
            if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                page.mouse.click(float(x), float(y))
                result["fallback"] = "coordinates"
            else:
                result["ok"] = False
                result["error"] = "click without selector/coordinates"
    elif action == "wait":
        wait_ms = int(decision.get("wait_ms") or 800)
        page.wait_for_timeout(max(200, min(wait_ms, 8000)))
        result["wait_ms"] = wait_ms
    elif action == "note":
        result["note"] = decision.get("thought")
    elif action == "done":
        result["done"] = True
    else:
        page.wait_for_timeout(500)
        result["ok"] = False
        result["error"] = f"unknown action {action}"

    # small settle after any action
    page.wait_for_timeout(int(decision.get("wait_ms") or 600) if action == "click" else 200)
    return result


def _build_user_prompt(knowledge: GameKnowledge, observation: dict[str, Any], iteration: int, max_iters: int) -> str:
    elements = observation.get("elements") or []
    compact_elements = [
        {
            "selector": e.get("selector"),
            "text": e.get("text"),
            "tag": e.get("tag"),
            "disabled": e.get("disabled"),
            "x": e.get("x"),
            "y": e.get("y"),
        }
        for e in elements
    ]
    return (
        f"Iteration {iteration}/{max_iters}\n"
        f"Game slug: {knowledge.game_slug}\n"
        f"URL: {observation.get('url')}\n"
        f"Title: {observation.get('title')}\n\n"
        f"Known controls: {json.dumps(knowledge.controls, ensure_ascii=False)}\n"
        f"Known features: {json.dumps(knowledge.features, ensure_ascii=False)}\n"
        f"UI regions: {json.dumps(knowledge.ui_regions, ensure_ascii=False)}\n"
        f"Hypotheses: {json.dumps(knowledge.hypotheses[-8:], ensure_ascii=False)}\n\n"
        f"Interactive elements:\n{json.dumps(compact_elements, ensure_ascii=False)}\n\n"
        "Decide the next exploration step. Return JSON only."
    )


def _policy_from_knowledge(knowledge: GameKnowledge) -> PlayPolicy:
    spin = (
        knowledge.controls.get("spin")
        or knowledge.controls.get("Spin")
        or knowledge.controls.get("play")
    )
    if not spin:
        raise RuntimeError(
            "Model finished without discovering a spin control. "
            "Increase --iterations or inspect /data/knowledge."
        )

    # crude pacing from hypotheses if present
    spin_delay_ms = 1000
    post_spin_wait_ms = 1200
    for hypo in knowledge.hypotheses:
        lower = hypo.lower()
        if "ms" in lower and "spin" in lower:
            digits = "".join(ch if ch.isdigit() else " " for ch in lower).split()
            if digits:
                try:
                    val = int(digits[0])
                    if 200 <= val <= 8000:
                        post_spin_wait_ms = val
                except ValueError:
                    pass

    return PlayPolicy(
        game_slug=knowledge.game_slug,
        start_url=knowledge.start_url,
        spin_selector=spin,
        busy_indicator=knowledge.controls.get("busy"),
        spin_delay_ms=spin_delay_ms,
        post_spin_wait_ms=post_spin_wait_ms,
        learned_from=f"model:{knowledge.model}",
        notes=[
            f"features={len(knowledge.features)}",
            f"controls={list(knowledge.controls)}",
            *knowledge.hypotheses[:5],
        ],
        extras={
            "features": knowledge.features,
            "controls": knowledge.controls,
            "ui_regions": knowledge.ui_regions,
            "iterations": len(knowledge.iteration_log),
        },
    )


def _looks_like_bot_wall(page: Page) -> str | None:
    """Return a reason if the page is a WAF/captcha wall instead of the game."""
    title = (page.title() or "").lower()
    body = ""
    try:
        body = (page.inner_text("body") or "").lower()
    except Exception:  # noqa: BLE001
        pass
    url = page.url.lower()
    markers = (
        "just a moment",
        "attention required",
        "security verification",
        "verify you are human",
        "cf-challenge",
        "cloudflare",
        "performing security verification",
    )
    blob = f"{title}\n{body}\n{url}"
    if any(m in blob for m in markers):
        return "Blocked by Cloudflare/bot verification — game UI is not reachable from this network"
    return None


def learn_with_model(
    page: Page,
    *,
    client: ModelClient,
    game_slug: str,
    start_url: str,
    iterations: int = 25,
) -> tuple[PlayPolicy, GameKnowledge]:
    page.goto(start_url, wait_until="domcontentloaded")
    page.wait_for_timeout(800)

    knowledge = GameKnowledge(
        game_slug=game_slug,
        start_url=start_url,
        model=client.model,
    )

    wall = _looks_like_bot_wall(page)
    if wall:
        knowledge.hypotheses.append(wall)
        knowledge.iteration_log.append(
            {
                "iteration": 0,
                "thought": wall,
                "decision": {"action": "note"},
                "exec": {"ok": False, "error": wall},
                "url": page.url,
                "title": page.title(),
            }
        )
        raise LearnError(wall, knowledge)

    for i in range(1, iterations + 1):
        observation = page_observation(page)
        wall = _looks_like_bot_wall(page)
        if wall:
            knowledge.hypotheses.append(wall)
            knowledge.iteration_log.append(
                {
                    "iteration": i,
                    "thought": wall,
                    "decision": {"action": "note"},
                    "exec": {"ok": False, "error": wall},
                }
            )
            raise LearnError(wall, knowledge)

        decision = client.chat_json(
            system=SYSTEM_PROMPT,
            user_text=_build_user_prompt(knowledge, observation, i, iterations),
            image_b64=observation.get("screenshot_b64"),
        )
        knowledge.merge_discovery(decision.get("discovery") if isinstance(decision, dict) else None)
        exec_result = _execute_action(page, decision)
        knowledge.iteration_log.append(
            {
                "iteration": i,
                "thought": decision.get("thought"),
                "decision": {
                    k: decision.get(k)
                    for k in ("action", "selector", "x", "y", "wait_ms")
                },
                "exec": exec_result,
                "controls": dict(knowledge.controls),
                "features": list(knowledge.features),
            }
        )

        if (decision.get("action") or "").lower() == "done" and knowledge.controls.get("spin"):
            knowledge.ready_to_play = True
            break
        if knowledge.ready_to_play and knowledge.controls.get("spin") and i >= min(8, iterations):
            break

    # If model never said done but found spin, still build policy
    if "spin" not in knowledge.controls:
        # last-chance: ask model to only pick spin selector from current DOM
        observation = page_observation(page)
        decision = client.chat_json(
            system=SYSTEM_PROMPT,
            user_text=(
                _build_user_prompt(knowledge, observation, iterations, iterations)
                + "\nFINAL: You must identify the spin/play control now. "
                "Set discovery.controls.spin and action=done."
            ),
            image_b64=observation.get("screenshot_b64"),
        )
        knowledge.merge_discovery(decision.get("discovery"))
        knowledge.iteration_log.append(
            {"iteration": "final", "thought": decision.get("thought"), "decision": decision}
        )

    try:
        policy = _policy_from_knowledge(knowledge)
    except RuntimeError as exc:
        raise LearnError(str(exc), knowledge) from exc
    return policy, knowledge
