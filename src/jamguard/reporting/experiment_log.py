"""Structured experiment logging helpers."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any


def log_experiment(payload: Any, output_path: Path) -> None:
    """Persist experiment context/results as JSON for reproducibility."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = asdict(payload) if is_dataclass(payload) else payload
    output_path.write_text(json.dumps(content, indent=2, default=str), encoding="utf-8")
