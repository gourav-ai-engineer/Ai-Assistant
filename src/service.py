from __future__ import annotations

import logging
import random
from dataclasses import dataclass
from pathlib import Path

from .automation import open_platforms
from .config import Settings
from .github_worker import GitHubPublisher, PublishResult
from .llm import generate_with_llm
from .notifier import notify
from .problems import PROBLEMS, Problem
from .solver import GeneratedSolution, generate_reference_solution
from .tracker import ProgressTracker
from .validator import ValidationResult, validate

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunResult:
    problem: Problem
    validation: ValidationResult
    published: PublishResult
    generation_source: str


def choose_problem(slug: str | None = None) -> Problem:
    if slug:
        for problem in PROBLEMS:
            if problem.slug == slug:
                return problem
        raise ValueError(f"Unknown problem: {slug}")
    return random.choice(PROBLEMS)


def run_once(settings: Settings, slug: str | None = None) -> RunResult:
    settings.ensure_directories()
    problem = choose_problem(slug)
    logger.info("Selected problem: %s", problem.name)

    if settings.open_platforms:
        open_platforms(problem)
    notify(problem)

    generated: GeneratedSolution = generate_reference_solution(problem)
    generation_source = "reference"

    if settings.llm_api_key:
        try:
            llm_source = generate_with_llm(
                problem,
                api_key=settings.llm_api_key,
                base_url=settings.llm_base_url,
                model=settings.llm_model,
            )
            # Keep the generated candidate available for review. The trusted reference
            # implementation remains the validator oracle; arbitrary LLM code is never
            # executed automatically.
            candidate_path = settings.generated_dir / f"{problem.slug}_llm.py"
            candidate_path.write_text(llm_source, encoding="utf-8")
            generation_source = "llm+reference"
            logger.info("Saved optional LLM candidate to %s", candidate_path)
        except Exception as exc:  # API/network/provider failures should not kill the run
            logger.warning("LLM generation unavailable, using reference solution: %s", exc)

    validation = validate(problem)
    publisher = GitHubPublisher(
        repo=settings.github_repo,
        token=settings.github_token,
        branch=settings.github_branch,
        local_dir=settings.generated_dir,
    )
    published = publisher.publish(
        slug=problem.slug,
        source=generated.source,
        enabled=settings.auto_publish,
    )

    tracker = ProgressTracker(settings.data_dir / "progress.jsonl")
    tracker.record(
        problem=problem.name,
        slug=problem.slug,
        passed=validation.passed,
        published=published.published,
        source=generation_source,
    )

    return RunResult(
        problem=problem,
        validation=validation,
        published=published,
        generation_source=generation_source,
    )
