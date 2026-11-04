-- Blue Wave catalog schema
-- Providers and games live in separate tables (one provider → many games).

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS providers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug            TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    website_url     TEXT,
    country_code    CHAR(2),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    source          TEXT NOT NULL DEFAULT 'seed',
    source_ref      TEXT,
    collected_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS games (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id     UUID NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
    slug            TEXT NOT NULL,
    name            TEXT NOT NULL,
    release_date    DATE,
    game_type       TEXT NOT NULL DEFAULT 'slot',
    rtp_percent     NUMERIC(5, 2),
    volatility      TEXT,
    demo_url        TEXT,
    thumbnail_url   TEXT,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    source          TEXT NOT NULL DEFAULT 'seed',
    source_ref      TEXT,
    metadata        JSONB NOT NULL DEFAULT '{}'::jsonb,
    collected_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT games_provider_slug_unique UNIQUE (provider_id, slug),
    CONSTRAINT games_rtp_range CHECK (
        rtp_percent IS NULL OR (rtp_percent >= 0 AND rtp_percent <= 100)
    )
);

CREATE INDEX IF NOT EXISTS idx_games_provider_id ON games (provider_id);
CREATE INDEX IF NOT EXISTS idx_games_release_date ON games (release_date DESC NULLS LAST);
CREATE INDEX IF NOT EXISTS idx_games_name ON games (name);
CREATE INDEX IF NOT EXISTS idx_providers_name ON providers (name);

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS providers_set_updated_at ON providers;
CREATE TRIGGER providers_set_updated_at
    BEFORE UPDATE ON providers
    FOR EACH ROW EXECUTE PROCEDURE set_updated_at();

DROP TRIGGER IF EXISTS games_set_updated_at ON games;
CREATE TRIGGER games_set_updated_at
    BEFORE UPDATE ON games
    FOR EACH ROW EXECUTE PROCEDURE set_updated_at();
