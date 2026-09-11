from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent

from .problems import Problem


@dataclass(frozen=True)
class GeneratedSolution:
    problem: Problem
    code: str
    source: str


_FUNCTION_BODIES = {
    "two-sum": """def solution(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return [seen[complement], i]
        seen[value] = i
    return []
""",
    "palindrome-number": """def solution(x: int) -> bool:
    if x < 0:
        return False
    return str(x) == str(x)[::-1]
""",
    "valid-parentheses": """def solution(s: str) -> bool:
    pairs = {')': '(', ']': '[', '}': '{'}
    stack: list[str] = []
    for char in s:
        if char in '([{':
            stack.append(char)
        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
        else:
            return False
    return not stack
""",
    "maximum-subarray": """def solution(nums: list[int]) -> int:
    if not nums:
        raise ValueError('maximum_subarray requires at least one number')
    best = current = nums[0]
    for value in nums[1:]:
        current = max(value, current + value)
        best = max(best, current)
    return best
""",
}


def generate_reference_solution(problem: Problem) -> GeneratedSolution:
    body = _FUNCTION_BODIES[problem.slug]
    source = dedent(
        f'''"""Generated solution for {problem.name}."""

{body}

if __name__ == "__main__":
    print("Solution ready: {problem.name}")
'''
    ).strip() + "\n"
    return GeneratedSolution(problem=problem, code=body.strip() + "\n", source=source)
