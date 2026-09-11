"""Backward-compatible root imports for the v2 assistant."""

from src.problems import PROBLEMS, Problem, get_problem
from src.service import choose_problem
from src.solver import generate_reference_solution


def select_problem() -> Problem:
    return choose_problem()


def generate_code(problem: Problem) -> str:
    return generate_reference_solution(problem).code

__all__ = ["PROBLEMS", "Problem", "get_problem", "select_problem", "generate_code"]
