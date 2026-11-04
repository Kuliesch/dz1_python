"""Blue Wave player — learn to play a demo game, then record gameplay video.

Workflow:
  1) learn  — open browser, discover controls, measure pacing, save policy
  2) record — reload policy, play N spins, save Playwright video + event log

By default uses the local mock slot fixture so the pipeline runs without
external demo URLs. Pass --url to target a permitted demo page.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

from browser import browser_page
from learner import learn_game
from paths import EVENTS, FIXTURES, POLICIES, RECORDINGS, ensure_data_dirs
from player import play_with_policy
from policy import PlayPolicy


def mock_url() -> str:
    return FIXTURES.joinpath("mock_slot.html").resolve().as_uri()


def resolve_url(url: str | None) -> str:
    if url:
        return url
    return os.environ.get("GAME_URL") or mock_url()


def policy_path(game_slug: str) -> Path:
    return POLICIES / f"{game_slug}.json"


def cmd_learn(args: argparse.Namespace) -> int:
    ensure_data_dirs()
    start_url = resolve_url(args.url)
    practice = getattr(args, "learn_spins", None) or 3
    with browser_page(headless=not args.headed) as (_pw, _browser, page):
        policy = learn_game(
            page,
            game_slug=args.game,
            start_url=start_url,
            practice_spins=practice,
        )
        if args.max_spins:
            policy.max_spins = args.max_spins
    out = policy.save(policy_path(args.game))
    print(json.dumps({"ok": True, "phase": "learn", "policy": str(out), "notes": policy.notes}, indent=2))
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    ensure_data_dirs()
    path = policy_path(args.game)
    if not path.exists():
        raise SystemExit(
            f"No policy for '{args.game}'. Run learn first: python -m main learn --game {args.game}"
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

    # cleanup temp context dir
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
            indent=2,
        )
    )
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    """Learn then record in one shot (default container entrypoint)."""
    learn_args = argparse.Namespace(
        game=args.game,
        url=args.url,
        headed=args.headed,
        max_spins=args.learn_spins,
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
    parser = argparse.ArgumentParser(description="Blue Wave player container")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--game", default="mock-slot", help="Game slug / policy name")
        p.add_argument("--url", default=None, help="Demo URL (default: local mock fixture)")
        p.add_argument("--headed", action="store_true", help="Show browser UI")
        p.add_argument("--max-spins", type=int, default=None, help="Spins for record phase")

    learn = sub.add_parser("learn", help="Discover controls and save a play policy")
    add_common(learn)
    learn.add_argument("--learn-spins", type=int, default=3, help="Practice spins while learning")
    learn.set_defaults(func=cmd_learn)

    record = sub.add_parser("record", help="Play with a learned policy and record video")
    add_common(record)
    record.set_defaults(func=cmd_record)

    run = sub.add_parser("run", help="Learn first, then record (default pipeline)")
    add_common(run)
    run.add_argument("--learn-spins", type=int, default=3, help="Practice spins during learn")
    run.set_defaults(func=cmd_run, max_spins=10)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
