from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    interval_seconds: int = 86400
    open_platforms: bool = False
    auto_publish: bool = False
    github_repo: str | None = None
    github_token: str | None = None
    github_branch: str = "main"
    llm_api_key: str | None = None
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"
    data_dir: Path = Path("data")
    generated_dir: Path = Path("generated")

    @classmethod
    def from_env(cls) -> "Settings":
        interval = int(os.getenv("AI_ASSISTANT_INTERVAL", "86400"))
        if interval < 1:
            raise ValueError("AI_ASSISTANT_INTERVAL must be >= 1")
        return cls(
            interval_seconds=interval,
            open_platforms=os.getenv("AI_ASSISTANT_OPEN_PLATFORMS", "false").lower() == "true",
            auto_publish=os.getenv("AI_ASSISTANT_AUTO_PUBLISH", "false").lower() == "true",
            github_repo=os.getenv("GITHUB_REPO") or None,
            github_token=os.getenv("GITHUB_TOKEN") or None,
            github_branch=os.getenv("GITHUB_BRANCH", "main"),
            llm_api_key=os.getenv("OPENAI_API_KEY") or None,
            llm_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
            llm_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        )

    def ensure_directories(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.generated_dir.mkdir(parents=True, exist_ok=True)
