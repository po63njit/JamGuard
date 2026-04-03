"""Generate lightweight report artifacts for capstone deliverables."""

from __future__ import annotations

from pathlib import Path

from jamguard.data.models import AnalysisResult


def write_markdown_summary(result: AnalysisResult, output_path: Path) -> None:
    """Write analysis metrics to a markdown report file."""
    lines = [f"# {result.name}", "", "## Metrics"]
    lines.extend(f"- **{k}**: {v:.6g}" for k, v in sorted(result.metrics.items()))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # TODO: export capstone-ready figures and references.
