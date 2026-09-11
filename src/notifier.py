from __future__ import annotations

import logging

from .problems import Problem

logger = logging.getLogger(__name__)


def notify(problem: Problem) -> None:
    message = f"Today's problem: {problem.name}\nHint: {problem.hint}"
    try:
        from plyer import notification  # type: ignore
    except ImportError:
        logger.info("Notification: %s", message.replace("\n", " | "))
        return
    try:
        notification.notify(title="AI Coding Assistant", message=message, timeout=8)
    except Exception as exc:  # pragma: no cover - platform dependent
        logger.warning("Desktop notification unavailable: %s", exc)
