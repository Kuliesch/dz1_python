"""OpenAI-compatible chat/vision client for the player learning agent.

Configure via env (do not commit secrets):
  PLAYER_API_KEY   — required for model learning
  PLAYER_API_BASE  — default https://api.openai.com/v1
  PLAYER_MODEL     — default gpt-4o-mini
"""

from __future__ import annotations

import json
import os
import re
from typing import Any

import httpx


class ModelError(RuntimeError):
    pass


def api_key() -> str | None:
    return os.environ.get("PLAYER_API_KEY") or os.environ.get("OPENAI_API_KEY")


def api_base() -> str:
    return os.environ.get("PLAYER_API_BASE", "https://api.openai.com/v1").rstrip("/")


def model_name() -> str:
    return os.environ.get("PLAYER_MODEL", "gpt-4o-mini")


class ModelClient:
    def __init__(
        self,
        *,
        key: str | None = None,
        base: str | None = None,
        model: str | None = None,
        timeout_sec: float = 90.0,
    ) -> None:
        self.key = key if key is not None else api_key()
        self.base = (base or api_base()).rstrip("/")
        self.model = model or model_name()
        self.timeout_sec = timeout_sec
        if not self.key:
            raise ModelError(
                "PLAYER_API_KEY (or OPENAI_API_KEY) is required for model-based learning"
            )

    def chat(
        self,
        *,
        system: str,
        user_text: str,
        image_b64: str | None = None,
        image_mime: str = "image/png",
    ) -> str:
        user_content: list[dict[str, Any]] = [{"type": "text", "text": user_text}]
        if image_b64:
            user_content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{image_mime};base64,{image_b64}",
                        "detail": "low",
                    },
                }
            )

        payload = {
            "model": self.model,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_content},
            ],
        }
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }
        url = f"{self.base}/chat/completions"
        with httpx.Client(timeout=self.timeout_sec) as client:
            response = client.post(url, headers=headers, json=payload)
            if response.status_code >= 400:
                raise ModelError(
                    f"model API {response.status_code}: {response.text[:800]}"
                )
            data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ModelError(f"unexpected model response: {data!r}") from exc

    def chat_json(
        self,
        *,
        system: str,
        user_text: str,
        image_b64: str | None = None,
    ) -> dict[str, Any]:
        raw = self.chat(system=system, user_text=user_text, image_b64=image_b64)
        return parse_json_object(raw)


def parse_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        value = json.loads(text)
        if isinstance(value, dict):
            return value
    except json.JSONDecodeError:
        pass

    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        return json.loads(fence.group(1))

    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        return json.loads(text[start : end + 1])

    raise ModelError(f"model did not return JSON object: {text[:400]}")
