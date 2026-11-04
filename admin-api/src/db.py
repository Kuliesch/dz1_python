"""Database access for Blue Wave admin-api."""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Iterator

import psycopg
from psycopg.rows import dict_row


def database_url() -> str:
    return os.environ.get(
        "DATABASE_URL",
        "postgresql://bluewave:bluewave@db:5432/bluewave",
    )


@contextmanager
def connect() -> Iterator[psycopg.Connection]:
    with psycopg.connect(database_url(), row_factory=dict_row) as conn:
        yield conn


def list_providers(conn: psycopg.Connection, *, active_only: bool = False) -> list[dict[str, Any]]:
    sql = """
        SELECT
            p.id::text AS id,
            p.slug,
            p.name,
            p.website_url,
            p.country_code,
            p.is_active,
            p.source,
            p.collected_at,
            COUNT(g.id) FILTER (WHERE g.is_active) AS games_count
        FROM providers p
        LEFT JOIN games g ON g.provider_id = p.id
    """
    if active_only:
        sql += " WHERE p.is_active = TRUE"
    sql += " GROUP BY p.id ORDER BY p.name"
    return list(conn.execute(sql).fetchall())


def get_provider(conn: psycopg.Connection, slug: str) -> dict[str, Any] | None:
    return conn.execute(
        """
        SELECT
            id::text AS id, slug, name, website_url, country_code,
            is_active, source, source_ref, collected_at, created_at, updated_at
        FROM providers
        WHERE slug = %s
        """,
        (slug,),
    ).fetchone()


def list_games(
    conn: psycopg.Connection,
    *,
    provider_slug: str | None = None,
    active_only: bool = False,
    limit: int = 200,
) -> list[dict[str, Any]]:
    clauses: list[str] = []
    params: list[Any] = []
    if provider_slug:
        clauses.append("p.slug = %s")
        params.append(provider_slug)
    if active_only:
        clauses.append("g.is_active = TRUE")
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    params.append(limit)
    sql = f"""
        SELECT
            g.id::text AS id,
            g.slug,
            g.name,
            g.release_date,
            g.game_type,
            g.rtp_percent,
            g.volatility,
            g.demo_url,
            g.is_active,
            g.source,
            g.collected_at,
            p.slug AS provider_slug,
            p.name AS provider_name
        FROM games g
        JOIN providers p ON p.id = g.provider_id
        {where}
        ORDER BY g.release_date DESC NULLS LAST, g.name
        LIMIT %s
    """
    return list(conn.execute(sql, params).fetchall())


def catalog_summary(conn: psycopg.Connection) -> dict[str, Any]:
    row = conn.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM providers WHERE is_active) AS providers,
            (SELECT COUNT(*) FROM games WHERE is_active) AS games,
            (SELECT COUNT(*) FROM games WHERE is_active AND release_date IS NOT NULL) AS games_with_release_date,
            (SELECT MAX(collected_at) FROM games) AS last_game_collected_at
        """
    ).fetchone()
    assert row is not None
    return dict(row)
