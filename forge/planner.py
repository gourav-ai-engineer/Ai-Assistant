from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol

from .types import ForgeTask, ToolCall


SYSTEM_PROMPT = """You are Forge, an autonomous software engineer. Work only inside the supplied workspace.
Inspect before editing. Make the smallest safe change that satisfies the request. After edits, run tests.
Never access secrets, never exfiltrate credentials, and never use shell strings with untrusted interpolation.
Return one JSON object: {\"steps\":[{\"tool\":str,\"arguments\":dict,\"reason\":str}],\"summary\":str}.
Allowed tools: repo_tree, read_file, write_file, git_status, git_diff, run_tests.
"""


class Planner(Protocol):
    def plan(self, task: ForgeTask, context: str) -> tuple[ToolCall, ...]: ...


@dataclass(frozen=True)
class OfflinePlanner:
    """Deterministic fallback that demonstrates the inspect->test loop without an API key."""

    def plan(self, task: ForgeTask, context: str) -> tuple[ToolCall, ...]:
        return (
            ToolCall("repo_tree", reason="Inspect the repository before changes."),
            ToolCall("git_status", reason="Establish the initial working-tree state."),
            ToolCall("run_tests", reason="Establish a baseline before editing."),
        )


@dataclass(frozen=True)
class JSONPlanner:
    """Adapter for a model response already returned as JSON."""

    def parse(self, raw: str) -> tuple[ToolCall, ...]:
        payload = json.loads(raw)
        if not isinstance(payload, dict) or not isinstance(payload.get("steps"), list):
            raise ValueError("Planner response must contain a steps list")
        calls: list[ToolCall] = []
        for item in payload["steps"]:
            if not isinstance(item, dict) or not isinstance(item.get("tool"), str):
                raise ValueError("Invalid tool step")
            calls.append(ToolCall(item["tool"], item.get("arguments") or {}, item.get("reason", "")))
        return tuple(calls)
