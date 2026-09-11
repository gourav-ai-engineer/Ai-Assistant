from src.problems import PROBLEMS, get_problem
from src.validator import validate


def test_all_reference_solutions_pass() -> None:
    assert PROBLEMS
    for problem in PROBLEMS:
        result = validate(problem)
        assert result.passed, (problem.name, result.failures)


def test_problem_lookup() -> None:
    assert get_problem("two-sum").name == "Two Sum"
