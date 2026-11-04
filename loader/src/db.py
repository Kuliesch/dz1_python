"""Database helpers for the Blue Wave catalog loader."""

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


def upsert_provider(conn: psycopg.Connection, provider: dict[str, Any]) -> str:
    row = conn.execute(
        """
        INSERT INTO providers (slug, name, website_url, country_code, source, source_ref, collected_at)
        VALUES (%(slug)s, %(name)s, %(website_url)s, %(country_code)s, %(source)s, %(source_ref)s, NOW())
        ON CONFLICT (slug) DO UPDATE SET
            name = EXCLUDED.name,
            website_url = COALESCE(EXCLUDED.website_url, providers.website_url),
            country_code = COALESCE(EXCLUDED.country_code, providers.country_code),
            source = EXCLUDED.source,
            source_ref = EXCLUDED.source_ref,
            collected_at = NOW(),
            is_active = TRUE
        RETURNING id::text AS id
        """,
        provider,
    ).fetchone()
    assert row is not None
    return row["id"]


def upsert_game(conn: psycopg.Connection, game: dict[str, Any]) -> str:
    row = conn.execute(
        """
        INSERT INTO games (
            provider_id, slug, name, release_date, game_type,
            rtp_percent, volatility, demo_url, thumbnail_url,
            source, source_ref, metadata, collected_at
        )
        VALUES (
            %(provider_id)s, %(slug)s, %(name)s, %(release_date)s, %(game_type)s,
            %(rtp_percent)s, %(volatility)s, %(demo_url)s, %(thumbnail_url)s,
            %(source)s, %(source_ref)s, %(metadata)s::jsonb, NOW()
        )
        ON CONFLICT (provider_id, slug) DO UPDATE SET
            name = EXCLUDED.name,
            release_date = COALESCE(EXCLUDED.release_date, games.release_date),
            game_type = EXCLUDED.game_type,
            rtp_percent = COALESCE(EXCLUDED.rtp_percent, games.rtp_percent),
            volatility = COALESCE(EXCLUDED.volatility, games.volatility),
            demo_url = COALESCE(EXCLUDED.demo_url, games.demo_url),
            thumbnail_url = COALESCE(EXCLUDED.thumbnail_url, games.thumbnail_url),
            source = EXCLUDED.source,
            source_ref = EXCLUDED.source_ref,
            metadata = EXCLUDED.metadata,
            collected_at = NOW(),
            is_active = TRUE
        RETURNING id::text AS id
        """,
        game,
    ).fetchone()
    assert row is not None
    return row["id"]


def catalog_stats(conn: psycopg.Connection) -> dict[str, Any]:
    row = conn.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM providers WHERE is_active) AS providers,
            (SELECT COUNT(*) FROM games WHERE is_active) AS games,
            (SELECT COUNT(*) FROM games WHERE is_active AND release_date IS NOT NULL) AS games_with_release_date
        """
    ).fetchone()
    assert row is not None
    return dict(row)
