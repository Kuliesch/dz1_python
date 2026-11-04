"""Blue Wave player — pass a game, learn it with a model, then record video.

Flow:
  1) Receive game (slug + URL)
  2) Open browser
  3) Over many iterations a vision/chat model explores UI, features, controls
  4) Save knowledge + play policy
  5) (optional) record gameplay video using the learned policy

API key via env: PLAYER_API_KEY (never commit secrets).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

from agent_learner import LearnError, learn_with_model
from browser import browser_page
from learner import learn_game
from model_client import ModelClient, ModelError, api_key, model_name
from paths import EVENTS, FIXTURES, KNOWLEDGE, POLICIES, RECORDINGS, ensure_data_dirs
from player import play_with_policy
from policy import PlayPolicy


def mock_url() -> str:
    return FIXTURES.joinpath("mock_slot.html").resolve().as_uri()


def resolve_url(url: str | None) -> str:
    if url:
        return url
    env_url = os.environ.get("GAME_URL")
    if env_url:
        return env_url
    return mock_url()


def policy_path(game_slug: str) -> Path:
    return POLICIES / f"{game_slug}.json"


def knowledge_path(game_slug: str) -> Path:
    return KNOWLEDGE / f"{game_slug}.json"


def cmd_learn(args: argparse.Namespace) -> int:
    ensure_data_dirs()
    start_url = resolve_url(args.url)
    mode = args.mode
    if mode == "auto":
        mode = "model" if api_key() else "heuristic"

    knowledge_out = None
    try:
        with browser_page(headless=not args.headed) as (_pw, _browser, page):
            if mode == "model":
                try:
                    client = ModelClient(model=args.model or None)
                except ModelError as exc:
                    raise SystemExit(str(exc)) from exc
                try:
                    policy, knowledge = learn_with_model(
                        page,
                        client=client,
                        game_slug=args.game,
                        start_url=start_url,
                        iterations=args.iterations,
                    )
                except LearnError as exc:
                    if exc.knowledge is not None:
                        knowledge_out = exc.knowledge.save(knowledge_path(args.game))
                    raise
                knowledge_out = knowledge.save(knowledge_path(args.game))
            else:
                policy = learn_game(
                    page,
                    game_slug=args.game,
                    start_url=start_url,
                    practice_spins=args.learn_spins,
                )

            if args.max_spins:
                policy.max_spins = args.max_spins
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "phase": "learn",
                    "mode": mode,
                    "game": args.game,
                    "url": start_url,
                    "error": str(exc),
                    "knowledge": str(knowledge_out) if knowledge_out else None,
                    "hint": (
                        "If this is Cloudflare/403, run player on a machine/network that can open "
                        "Stake in a normal browser, or supply a provider demo URL without WAF."
                    ),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    out = policy.save(policy_path(args.game))
    print(
        json.dumps(
            {
                "ok": True,
                "phase": "learn",
                "mode": mode,
                "game": args.game,
                "url": start_url,
                "model": model_name() if mode == "model" else None,
                "iterations": args.iterations if mode == "model" else args.learn_spins,
                "policy": str(out),
                "knowledge": str(knowledge_out) if knowledge_out else None,
                "controls": policy.extras.get("controls") if mode == "model" else {"spin": policy.spin_selector},
                "features": policy.extras.get("features") if mode == "model" else [],
                "notes": policy.notes,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    ensure_data_dirs()
    path = policy_path(args.game)
    if not path.exists():
        raise SystemExit(
            f"No policy for '{args.game}'. Run learn first with the game URL and PLAYER_API_KEY."
        )
    policy = PlayPolicy.load(path)
    if args.url:
        policy.start_url = args.url
    if args.max_spins:
        policy.max_spins = args.max_spins

    session_dir = RECORDINGS / args.game / "tmp"
    if session_dir.exists():
        shutil.rmtree(session_dir)
    session_dir.mkdir(parents=True)

    events_file = EVENTS / f"{args.game}.json"
    with browser_page(headless=not args.headed, record_dir=session_dir) as (_pw, _browser, page):
        events = play_with_policy(
            page,
            policy,
            max_spins=policy.max_spins,
            events_path=events_file,
        )

    videos = sorted(session_dir.glob("*.webm"))
    final_video = RECORDINGS / f"{args.game}.webm"
    if videos:
        shutil.move(str(videos[0]), final_video)
    else:
        final_video = None  # type: ignore[assignment]

    shutil.rmtree(session_dir, ignore_errors=True)

    print(
        json.dumps(
            {
                "ok": True,
                "phase": "record",
                "game": args.game,
                "spins": len(events),
                "video": str(final_video) if final_video else None,
                "events": str(events_file),
                "policy": str(path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    learn_args = argparse.Namespace(
        game=args.game,
        url=args.url,
        headed=args.headed,
        max_spins=args.max_spins,
        learn_spins=args.learn_spins,
        iterations=args.iterations,
        mode=args.mode,
        model=args.model,
    )
    record_args = argparse.Namespace(
        game=args.game,
        url=args.url,
        headed=args.headed,
        max_spins=args.max_spins,
    )
    rc = cmd_learn(learn_args)
    if rc != 0:
        return rc
    return cmd_record(record_args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Blue Wave player: pass a game, learn UI with a model, record video"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--game", required=True, help="Game slug (identity for policy/knowledge)")
        p.add_argument(
            "--url",
            default=None,
            help="Game demo URL to open (or env GAME_URL; mock fixture if omitted)",
        )
        p.add_argument("--headed", action="store_true", help="Show browser UI")
        p.add_argument("--max-spins", type=int, default=None, help="Spins for record phase")

    def add_learn_flags(p: argparse.ArgumentParser) -> None:
        p.add_argument(
            "--mode",
            choices=["auto", "model", "heuristic"],
            default="auto",
            help="Learning mode (auto uses model when PLAYER_API_KEY is set)",
        )
        p.add_argument(
            "--model",
            default=None,
            help="Override PLAYER_MODEL (OpenAI-compatible model id)",
        )
        p.add_argument(
            "--iterations",
            type=int,
            default=int(os.environ.get("PLAYER_LEARN_ITERATIONS", "25")),
            help="Model exploration iterations (default 25)",
        )
        p.add_argument(
            "--learn-spins",
            type=int,
            default=3,
            help="Heuristic practice spins (fallback mode only)",
        )

    learn = sub.add_parser("learn", help="Explore game UI with model over many iterations")
    add_common(learn)
    add_learn_flags(learn)
    learn.set_defaults(func=cmd_learn)

    record = sub.add_parser("record", help="Play with learned policy and record video")
    add_common(record)
    record.set_defaults(func=cmd_record)

    run = sub.add_parser("run", help="Learn then record")
    add_common(run)
    add_learn_flags(run)
    run.set_defaults(func=cmd_run, max_spins=10)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
