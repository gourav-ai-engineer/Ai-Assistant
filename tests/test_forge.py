from __future__ import annotations

from pathlib import Path

import pytest

from forge.engine import ForgeEngine
from forge.planner import JSONPlanner
from forge.types import ForgeTask, RunStatus, ToolCall
from forge.workspace import Workspace


def test_workspace_blocks_path_escape(tmp_path: Path) -> None:
    ws = Workspace(tmp_path)
    with pytest.raises(ValueError):
        ws.path("../outside.txt")


def test_write_requires_explicit_approval(tmp_path: Path) -> None:
    ws = Workspace(tmp_path)
    registry_task = ForgeTask("write", str(tmp_path), require_approval_for_write=True)
    report = ForgeEngine().run(registry_task, allow_writes=False)
    assert report.status is RunStatus.SUCCEEDED
    assert all(step.tool != "write_file" for step in report.steps)


def test_offline_engine_smoke(tmp_path: Path) -> None:
    (tmp_path / "test_sample.py").write_text("def test_ok(): assert 1 + 1 == 2\n", encoding="utf-8")
    report = ForgeEngine().run(ForgeTask("inspect", str(tmp_path)))
    assert report.status is RunStatus.SUCCEEDED
    assert {step.tool for step in report.steps} == {"repo_tree", "git_status", "run_tests"}


def test_planner_json_validation() -> None:
    planner = JSONPlanner()
    calls = planner.parse('{"steps":[{"tool":"repo_tree","arguments":{},"reason":"inspect"}]}')
    assert calls == (ToolCall("repo_tree", {}, "inspect"),)


def test_unknown_tool_fails(tmp_path: Path) -> None:
    from forge.tools import ToolRegistry
    result = ToolRegistry(Workspace(tmp_path)).execute(ToolCall("nope"))
    assert not result.ok
