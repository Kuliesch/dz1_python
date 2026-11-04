"""Blue Wave mounter — assemble raw player recordings into review cuts.

Reads:
  /data/recordings/<game>.webm
  /data/events/<game>.json   (optional)

Writes:
  /data/mounted/<game>_review.mp4
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from edit import MountError, build_review, load_events

DATA = Path("/data")
RECORDINGS = DATA / "recordings"
EVENTS = DATA / "events"
MOUNTED = DATA / "mounted"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mount Blue Wave gameplay into a review video")
    parser.add_argument("--game", default="mock-slot", help="Game slug (matches player output)")
    parser.add_argument(
        "--source",
        default=None,
        help="Override source video path (default: /data/recordings/<game>.webm)",
    )
    parser.add_argument(
        "--events",
        default=None,
        help="Override events JSON path (default: /data/events/<game>.json)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Override output path (default: /data/mounted/<game>_review.mp4)",
    )
    parser.add_argument("--title", default=None, help="Burn-in title (default: game slug)")
    parser.add_argument(
        "--subtitle",
        default="Blue Wave · gameplay review",
        help="Burn-in subtitle",
    )
    parser.add_argument(
        "--max-seconds",
        type=float,
        default=150.0,
        help="Max review length in seconds (default ~2.5 min)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    source = Path(args.source) if args.source else RECORDINGS / f"{args.game}.webm"
    events_path = Path(args.events) if args.events else EVENTS / f"{args.game}.json"
    output = Path(args.output) if args.output else MOUNTED / f"{args.game}_review.mp4"
    title = args.title or args.game.replace("-", " ").title()

    try:
        events = load_events(events_path)
        result = build_review(
            source=source,
            output=output,
            title=title,
            subtitle=args.subtitle,
            max_seconds=args.max_seconds,
            events=events,
        )
    except MountError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1

    print(
        json.dumps(
            {
                "ok": True,
                "game": args.game,
                "source": str(result.source),
                "output": str(result.output),
                "duration_sec": result.duration_sec,
                "spins": result.spins,
                "title": result.title,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
