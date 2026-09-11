"""Legacy entrypoint kept safe: no automatic git operations on import/run."""

from src.github_worker import GitHubPublisher


def make_commit(code: str) -> str:
    result = GitHubPublisher(repo=None, token=None).publish(
        slug="manual-solution",
        source=code,
        enabled=False,
    )
    return result.location


if __name__ == "__main__":
    print("Automatic git pushing is disabled by design. Use `python main.py --once` instead.")
