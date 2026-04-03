"""Run summary output utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_json_summary(payload: dict[str, Any], output_path: Path) -> None:
    """Write run summary dictionary as JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
