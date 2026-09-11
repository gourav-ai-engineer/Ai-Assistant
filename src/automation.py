from __future__ import annotations

import logging
import webbrowser

from .problems import Problem

logger = logging.getLogger(__name__)

PLATFORMS = {
    "leetcode": "https://leetcode.com/problemset/?difficulty=EASY",
    "hackerrank": "https://www.hackerrank.com/dashboard",
    "github": "https://github.com",
}


def open_platforms(problem: Problem | None = None) -> None:
    """Open useful coding platforms; failures never stop the assistant."""
    suffix = f"#{problem.slug}" if problem else ""
    for name, url in PLATFORMS.items():
        try:
            webbrowser.open(url)
            logger.info("Opened %s %s", name, suffix)
        except Exception as exc:  # pragma: no cover - OS/browser dependent
            logger.warning("Could not open %s: %s", name, exc)
