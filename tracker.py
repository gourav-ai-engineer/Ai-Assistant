"""Backward-compatible progress tracking wrapper."""

from pathlib import Path

from src.tracker import ProgressTracker


def track(problem) -> None:
    name = problem["name"] if isinstance(problem, dict) else problem.name
    slug = name.lower().replace(" ", "-")
    ProgressTracker(Path("data/progress.jsonl")).record(
        problem=name,
        slug=slug,
        passed=True,
        published=False,
        source="legacy-wrapper",
    )
