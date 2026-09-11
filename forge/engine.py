from __future__ import annotations

import time
import uuid
from dataclasses import dataclass

from .planner import OfflinePlanner, Planner
from .tools import ToolRegistry
from .types import ForgeTask, RunReport, RunStatus, StepRecord
from .workspace import Workspace


@dataclass
class ForgeEngine:
    """Small, testable agent runtime with explicit tool boundaries."""

    planner: Planner | None = None

    def run(self, task: ForgeTask, *, allow_writes: bool | None = None) -> RunReport:
        task_id = task.task_id or uuid.uuid4().hex[:12]
        started_at = RunReport.timestamp()
        workspace = Workspace(task.repo_path)
        approved = task.require_approval_for_write is False if allow_writes is None else allow_writes
        registry = ToolRegistry(workspace, allow_writes=approved)
        planner = self.planner or OfflinePlanner()
        calls = planner.plan(task, "")[: task.max_steps]
        records: list[StepRecord] = []

        for index, call in enumerate(calls, start=1):
            started = time.perf_counter()
            result = registry.execute(call)
            records.append(
                StepRecord(
                    index=index,
                    tool=call.name,
                    ok=result.ok,
                    output=result.output if result.ok else result.error,
                    duration_ms=(time.perf_counter() - started) * 1000,
                )
            )
            if not result.ok and call.name in {"write_file"}:
                return RunReport(task_id, RunStatus.BLOCKED, result.error, tuple(records), started_at, RunReport.timestamp())

        status = RunStatus.SUCCEEDED if all(r.ok for r in records) else RunStatus.FAILED
        summary = "Offline inspect/test cycle completed." if status is RunStatus.SUCCEEDED else "Agent cycle encountered a tool failure."
        return RunReport(task_id, status, summary, tuple(records), started_at, RunReport.timestamp())
