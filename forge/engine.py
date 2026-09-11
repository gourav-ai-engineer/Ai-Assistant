from __future__ import annotations

import time
import uuid
from dataclasses import dataclass

from .planner import OfflinePlanner, Planner
from .tools import ToolRegistry
from .types import ForgeTask, RunReport, RunStatus, StepRecord, ToolCall
from .workspace import Workspace


@dataclass
class ForgeEngine:
    """Agent runtime with an inspect -> plan -> act -> validate loop."""

    planner: Planner | None = None
    max_rounds: int = 3

    def _execute(self, registry: ToolRegistry, calls: tuple[ToolCall, ...], records: list[StepRecord], offset: int) -> None:
        for index, call in enumerate(calls, start=offset):
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

    def run(self, task: ForgeTask, *, allow_writes: bool | None = None) -> RunReport:
        if task.max_steps < 1 or task.max_steps > 100:
            raise ValueError("max_steps must be between 1 and 100")
        if self.max_rounds < 1 or self.max_rounds > 10:
            raise ValueError("max_rounds must be between 1 and 10")

        task_id = task.task_id or uuid.uuid4().hex[:12]
        started_at = RunReport.timestamp()
        workspace = Workspace(task.repo_path)
        approved = task.require_approval_for_write is False if allow_writes is None else allow_writes
        registry = ToolRegistry(workspace, allow_writes=approved)
        planner = self.planner or OfflinePlanner()
        records: list[StepRecord] = []

        # Establish a baseline that every planner can reason over.
        baseline = (ToolCall("repo_tree", reason="Inspect the repository before acting."),
                    ToolCall("git_status", reason="Establish the working-tree state."),
                    ToolCall("run_tests", reason="Establish a validation baseline."))
        self._execute(registry, baseline, records, 1)

        if isinstance(planner, OfflinePlanner):
            ok = all(step.ok for step in records)
            status = RunStatus.SUCCEEDED if ok else RunStatus.FAILED
            summary = "Offline inspect/test cycle completed." if ok else "Baseline validation failed."
            return RunReport(task_id, status, summary, tuple(records), started_at, RunReport.timestamp())

        context_parts = [f"{step.tool}: {'OK' if step.ok else 'ERROR'}\n{step.output}" for step in records]
        next_index = len(records) + 1
        rounds = 0
        while rounds < self.max_rounds and len(records) < task.max_steps:
            rounds += 1
            context = "\n\n".join(context_parts)[-40_000:]
            calls = planner.plan(task, context)[: task.max_steps - len(records)]
            if not calls:
                break
            self._execute(registry, calls, records, next_index)
            next_index = len(records) + 1
            context_parts = [f"{step.tool}: {'OK' if step.ok else 'ERROR'}\n{step.output}" for step in records]
            if records and records[-1].tool == "run_tests" and records[-1].ok:
                break

        ok = bool(records) and all(step.ok for step in records)
        status = RunStatus.SUCCEEDED if ok else RunStatus.FAILED
        summary = "Autonomous execution loop completed." if ok else "Agent execution needs another repair cycle."
        return RunReport(task_id, status, summary, tuple(records), started_at, RunReport.timestamp())
