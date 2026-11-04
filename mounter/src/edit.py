"""FFmpeg-based montage for Blue Wave gameplay recordings."""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class MountError(RuntimeError):
    pass


@dataclass
class MountResult:
    output: Path
    source: Path
    duration_sec: float | None
    title: str
    spins: int | None


def _which_ffmpeg() -> str:
    path = shutil.which("ffmpeg")
    if not path:
        raise MountError("ffmpeg not found in PATH")
    return path


def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise MountError(
            "ffmpeg failed:\n"
            + (proc.stderr or proc.stdout or f"exit {proc.returncode}")
        )


def probe_duration(path: Path) -> float | None:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return None
    proc = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    try:
        return float(proc.stdout.strip())
    except ValueError:
        return None


def load_events(events_path: Path | None) -> dict[str, Any]:
    if not events_path or not events_path.exists():
        return {}
    return json.loads(events_path.read_text(encoding="utf-8"))


def _escape_drawtext(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
        .replace("%", "\\%")
    )


def build_review(
    *,
    source: Path,
    output: Path,
    title: str,
    subtitle: str,
    max_seconds: float = 150.0,
    events: dict[str, Any] | None = None,
) -> MountResult:
    """Assemble a short review cut from a raw gameplay recording.

    Pipeline:
      1) trim/pad source to target length
      2) burn-in title + selected-episodes disclaimer
      3) write H.264 MP4 for distribution / later AI voice overlays
    """
    ffmpeg = _which_ffmpeg()
    if not source.exists():
        raise MountError(f"source video not found: {source}")

    output.parent.mkdir(parents=True, exist_ok=True)
    events = events or {}
    spins = events.get("spins")
    if isinstance(spins, int):
        spin_line = f"Spins captured: {spins}"
    else:
        spin_line = "Gameplay capture"

    title_esc = _escape_drawtext(title)
    sub_esc = _escape_drawtext(subtitle)
    spin_esc = _escape_drawtext(spin_line)
    disclaimer = _escape_drawtext("Selected episodes · not typical outcome frequency")
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font_opt = f"fontfile={font}:"

    # Scale to 1280x720, trim to max_seconds, overlay titles.
    filter_complex = (
        f"[0:v]scale=1280:720:force_original_aspect_ratio=decrease,"
        f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,"
        f"trim=duration={max_seconds},setpts=PTS-STARTPTS,"
        f"drawtext={font_opt}text='{title_esc}':x=40:y=40:fontsize=36:fontcolor=white:"
        f"box=1:boxcolor=black@0.55:boxborderw=12,"
        f"drawtext={font_opt}text='{sub_esc}':x=40:y=100:fontsize=22:fontcolor=white:"
        f"box=1:boxcolor=black@0.45:boxborderw=10,"
        f"drawtext={font_opt}text='{spin_esc}':x=40:y=h-90:fontsize=20:fontcolor=white:"
        f"box=1:boxcolor=black@0.45:boxborderw=8,"
        f"drawtext={font_opt}text='{disclaimer}':x=40:y=h-50:fontsize=18:fontcolor=yellow:"
        f"box=1:boxcolor=black@0.45:boxborderw=8[v]"
    )

    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(source),
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "23",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(output),
    ]
    _run(cmd)

    return MountResult(
        output=output,
        source=source,
        duration_sec=probe_duration(output),
        title=title,
        spins=spins if isinstance(spins, int) else None,
    )
