from src.config import Settings
from src.service import run_once


def test_run_once_end_to_end(tmp_path) -> None:
    settings = Settings(data_dir=tmp_path / "data", generated_dir=tmp_path / "generated")
    result = run_once(settings, slug="two-sum")
    assert result.validation.passed
    assert result.published.published is False
    assert (tmp_path / "generated").exists()
    assert (tmp_path / "data" / "progress.jsonl").exists()
