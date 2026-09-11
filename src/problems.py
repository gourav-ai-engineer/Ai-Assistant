from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class TestCase:
    args: tuple[Any, ...]
    expected: Any


@dataclass(frozen=True)
class Problem:
    name: str
    slug: str
    difficulty: str
    statement: str
    hint: str
    starter_code: str
    solver: Callable[..., Any]
    tests: tuple[TestCase, ...]


def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], i]
        seen[value] = i
    return []


def palindrome_number(x: int) -> bool:
    if x < 0:
        return False
    return str(x) == str(x)[::-1]


def valid_parentheses(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for char in s:
        if char in "([{":
            stack.append(char)
        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
        else:
            return False
    return not stack


def maximum_subarray(nums: list[int]) -> int:
    if not nums:
        raise ValueError("maximum_subarray requires at least one number")
    best = current = nums[0]
    for value in nums[1:]:
        current = max(value, current + value)
        best = max(best, current)
    return best


PROBLEMS: tuple[Problem, ...] = (
    Problem(
        name="Two Sum",
        slug="two-sum",
        difficulty="Easy",
        statement="Given an array of integers and a target, return the indices of two values whose sum equals the target.",
        hint="Use a dictionary to store previously seen values and look up the complement.",
        starter_code="def solution(nums: list[int], target: int) -> list[int]:\n    pass\n",
        solver=two_sum,
        tests=(
            TestCase(([2, 7, 11, 15], 9), [0, 1]),
            TestCase(([3, 2, 4], 6), [1, 2]),
            TestCase(([3, 3], 6), [0, 1]),
        ),
    ),
    Problem(
        name="Palindrome Number",
        slug="palindrome-number",
        difficulty="Easy",
        statement="Return true when an integer reads the same forward and backward.",
        hint="Negative numbers are not palindromes; strings make the comparison straightforward.",
        starter_code="def solution(x: int) -> bool:\n    pass\n",
        solver=palindrome_number,
        tests=(
            TestCase((121,), True),
            TestCase((-121,), False),
            TestCase((10,), False),
        ),
    ),
    Problem(
        name="Valid Parentheses",
        slug="valid-parentheses",
        difficulty="Easy",
        statement="Determine whether brackets are correctly opened and closed in the given string.",
        hint="Push opening brackets onto a stack and match every closing bracket against the top.",
        starter_code="def solution(s: str) -> bool:\n    pass\n",
        solver=valid_parentheses,
        tests=(
            TestCase(("()",), True),
            TestCase(("()[]{}",), True),
            TestCase(("(]",), False),
            TestCase(("([)]",), False),
            TestCase(("{[]}",), True),
        ),
    ),
    Problem(
        name="Maximum Subarray",
        slug="maximum-subarray",
        difficulty="Easy",
        statement="Find the contiguous subarray with the largest sum and return that sum.",
        hint="Kadane's algorithm keeps the best sum ending at the current position.",
        starter_code="def solution(nums: list[int]) -> int:\n    pass\n",
        solver=maximum_subarray,
        tests=(
            TestCase(([-2, 1, -3, 4, -1, 2, 1, -5, 4],), 6),
            TestCase(([1],), 1),
            TestCase(([5, 4, -1, 7, 8],), 23),
        ),
    ),
)


def get_problem(slug: str) -> Problem:
    for problem in PROBLEMS:
        if problem.slug == slug:
            return problem
    raise KeyError(f"Unknown problem slug: {slug}")
