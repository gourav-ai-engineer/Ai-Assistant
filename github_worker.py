"""Backward-compatible publishing wrapper."""

from src.github_worker import GitHubPublisher, PublishResult


def commit_code(code: str) -> PublishResult:
    """Store code locally; remote publishing is opt-in through the v2 service."""
    publisher = GitHubPublisher(repo=None, token=None)
    return publisher.publish(slug="legacy-solution", source=code, enabled=False)
