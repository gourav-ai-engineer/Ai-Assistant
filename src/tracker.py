from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ProgressTracker:
    def __init__(self, path: Path = Path("data/progress.jsonl")) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, *, problem: str, slug: str, passed: bool, published: bool, source: str) -> None:
        event: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "problem": problem,
            "slug": slug,
            "tests_passed": passed,
            "published": published,
            "source": source,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event) + "\n")

    def summary(self) -> dict[str, int]:
        total = passed = published = 0
        if not self.path.exists():
            return {"total": 0, "passed": 0, "published": 0}
        with self.path.open(encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                item = json.loads(line)
                total += 1
                passed += int(bool(item.get("tests_passed")))
                published += int(bool(item.get("published")))
        return {"total": total, "passed": passed, "published": published}
