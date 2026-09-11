from __future__ import annotations

import base64
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import requests

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PublishResult:
    published: bool
    location: str
    message: str


class GitHubPublisher:
    """Publish generated solutions through the GitHub Contents API.

    Without a token/repository, the assistant safely stores the solution locally.
    """

    def __init__(self, repo: str | None, token: str | None, branch: str = "main", local_dir: Path = Path("generated")) -> None:
        self.repo = repo
        self.token = token
        self.branch = branch
        self.local_dir = local_dir
        self.local_dir.mkdir(parents=True, exist_ok=True)

    def publish(self, *, slug: str, source: str, enabled: bool) -> PublishResult:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        filename = f"{slug}_{timestamp}.py"
        local_path = self.local_dir / filename
        local_path.write_text(source, encoding="utf-8")

        if not enabled:
            return PublishResult(False, str(local_path), "Local mode: publishing disabled")
        if not self.repo or not self.token:
            return PublishResult(False, str(local_path), "GitHub credentials not configured; kept local")

        path = f"generated/{filename}"
        url = f"https://api.github.com/repos/{self.repo}/contents/{path}"
        payload = {
            "message": f"feat: add generated solution for {slug}",
            "content": base64.b64encode(source.encode("utf-8")).decode("ascii"),
            "branch": self.branch,
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        try:
            response = requests.put(url, json=payload, headers=headers, timeout=20)
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.error("GitHub publish failed: %s", exc)
            return PublishResult(False, str(local_path), f"GitHub publish failed: {exc}")

        return PublishResult(True, f"https://github.com/{self.repo}/blob/{self.branch}/{path}", "Published to GitHub")
