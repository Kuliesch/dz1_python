"""Blue Wave admin-api — HTTP API for catalog and media status."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from db import catalog_summary, connect, get_provider, list_games, list_providers
from media import list_media

app = FastAPI(title="Blue Wave Admin API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _jsonable(value: Any) -> Any:
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, UUID):
        return str(value)
    return value


@app.get("/health")
def health() -> dict[str, str]:
    try:
        with connect() as conn:
            conn.execute("SELECT 1")
        db_status = "ok"
    except Exception as exc:  # noqa: BLE001
        db_status = f"error: {exc}"
    return {"status": "ok" if db_status == "ok" else "degraded", "db": db_status}


@app.get("/api/summary")
def summary() -> dict[str, Any]:
    with connect() as conn:
        data = catalog_summary(conn)
    media = list_media()
    return _jsonable(
        {
            "catalog": data,
            "media": {
                "recordings": len(media["recordings"]),
                "mounted": len(media["mounted"]),
                "policies": len(media["policies"]),
                "events": len(media["events"]),
            },
        }
    )


@app.get("/api/providers")
def providers(active_only: bool = Query(False)) -> list[dict[str, Any]]:
    with connect() as conn:
        rows = list_providers(conn, active_only=active_only)
    return _jsonable(rows)


@app.get("/api/providers/{slug}")
def provider(slug: str) -> dict[str, Any]:
    with connect() as conn:
        row = get_provider(conn, slug)
        if not row:
            raise HTTPException(status_code=404, detail="provider not found")
        games = list_games(conn, provider_slug=slug)
    return _jsonable({"provider": row, "games": games})


@app.get("/api/games")
def games(
    provider: str | None = Query(None, description="Filter by provider slug"),
    active_only: bool = Query(False),
    limit: int = Query(200, ge=1, le=1000),
) -> list[dict[str, Any]]:
    with connect() as conn:
        rows = list_games(conn, provider_slug=provider, active_only=active_only, limit=limit)
    return _jsonable(rows)


@app.get("/api/media")
def media() -> dict[str, Any]:
    return _jsonable(list_media())
