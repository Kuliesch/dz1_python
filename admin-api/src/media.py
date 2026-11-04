"""Inspect shared media volume artifacts from player/mounter."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any


def media_root() -> Path:
    return Path(os.environ.get("MEDIA_ROOT", "/data"))


def _file_info(path: Path) -> dict[str, Any]:
    stat = path.stat()
    return {
        "name": path.name,
        "path": str(path),
        "size_bytes": stat.st_size,
        "modified_at": stat.st_mtime,
    }


def list_media() -> dict[str, Any]:
    root = media_root()
    recordings = sorted((root / "recordings").glob("*.webm")) if (root / "recordings").exists() else []
    mounted = sorted((root / "mounted").glob("*.mp4")) if (root / "mounted").exists() else []
    events = sorted((root / "events").glob("*.json")) if (root / "events").exists() else []
    policies = sorted((root / "policies").glob("*.json")) if (root / "policies").exists() else []
    return {
        "root": str(root),
        "recordings": [_file_info(p) for p in recordings],
        "mounted": [_file_info(p) for p in mounted],
        "events": [_file_info(p) for p in events],
        "policies": [_file_info(p) for p in policies],
    }
