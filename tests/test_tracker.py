import json

from src.tracker import ProgressTracker


def test_tracker_records_jsonl(tmp_path) -> None:
    path = tmp_path / "progress.jsonl"
    tracker = ProgressTracker(path)
    tracker.record(problem="Two Sum", slug="two-sum", passed=True, published=False, source="reference")
    tracker.record(problem="Palindrome Number", slug="palindrome-number", passed=True, published=True, source="reference")

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["slug"] == "two-sum"
    assert tracker.summary() == {"total": 2, "passed": 2, "published": 1}
