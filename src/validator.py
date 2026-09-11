from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from .problems import Problem


@dataclass(frozen=True)
class ValidationResult:
    passed: bool
    total: int
    passed_cases: int
    duration_ms: float
    failures: tuple[str, ...]


def validate(problem: Problem) -> ValidationResult:
    failures: list[str] = []
    started = perf_counter()
    for index, case in enumerate(problem.tests, start=1):
        try:
            actual = problem.solver(*case.args)
            if actual != case.expected:
                failures.append(
                    f"case {index}: expected {case.expected!r}, got {actual!r}"
                )
        except Exception as exc:  # pragma: no cover - defensive safety net
            failures.append(f"case {index}: raised {type(exc).__name__}: {exc}")
    duration_ms = (perf_counter() - started) * 1000
    return ValidationResult(
        passed=not failures,
        total=len(problem.tests),
        passed_cases=len(problem.tests) - len(failures),
        duration_ms=duration_ms,
        failures=tuple(failures),
    )
