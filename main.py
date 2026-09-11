from __future__ import annotations

import argparse
import logging
import time

import schedule

from src.config import Settings
from src.service import run_once


def _run(settings: Settings, slug: str | None) -> None:
    result = run_once(settings, slug=slug)
    status = "PASS" if result.validation.passed else "FAIL"
    print(
        f"{result.problem.name}: {status} "
        f"({result.validation.passed_cases}/{result.validation.total} tests), "
        f"published={result.published.published}, source={result.generation_source}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Autonomous AI Coding Assistant")
    parser.add_argument("--once", action="store_true", help="run exactly one assistant cycle")
    parser.add_argument("--problem", help="problem slug, e.g. two-sum")
    parser.add_argument("--interval", type=int, help="recurring interval in seconds")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    settings = Settings.from_env()
    interval = args.interval or settings.interval_seconds
    if interval < 1:
        parser.error("--interval must be >= 1")

    if args.once:
        _run(settings, args.problem)
        return

    schedule.every(interval).seconds.do(_run, settings, args.problem)
    print(f"AI Assistant running every {interval} seconds. Press Ctrl+C to stop.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAI Assistant stopped.")


if __name__ == "__main__":
    main()
