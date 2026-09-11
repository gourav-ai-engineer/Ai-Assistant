from __future__ import annotations

from .types import ToolCall, ToolResult
from .workspace import Workspace


READ_ONLY = {"repo_tree", "read_file", "git_status", "git_diff", "run_tests"}
WRITE_TOOLS = {"write_file"}


class ToolRegistry:
    def __init__(self, workspace: Workspace, *, allow_writes: bool = False) -> None:
        self.workspace = workspace
        self.allow_writes = allow_writes

    def execute(self, call: ToolCall) -> ToolResult:
        try:
            if call.name == "repo_tree":
                return ToolResult(True, "\n".join(self.workspace.list_files()))
            if call.name == "read_file":
                return ToolResult(True, self.workspace.read(str(call.arguments["path"])))
            if call.name == "write_file":
                return ToolResult(
                    True,
                    self.workspace.write(
                        str(call.arguments["path"]),
                        str(call.arguments["content"]),
                        self.allow_writes,
                    ),
                )
            if call.name == "git_status":
                return self.workspace.run(["git", "status", "--short"])
            if call.name == "git_diff":
                return self.workspace.run(["git", "diff", "--", "."])
            if call.name == "run_tests":
                return self._run_tests()
            return ToolResult(False, "", f"unknown tool: {call.name}")
        except (KeyError, TypeError, ValueError, FileNotFoundError, PermissionError) as exc:
            return ToolResult(False, "", f"tool error: {exc}")

    def _run_tests(self) -> ToolResult:
        if (self.workspace.root / "pyproject.toml").exists() or (self.workspace.root / "pytest.ini").exists():
            return self.workspace.run(["python", "-m", "pytest", "-q"], timeout_seconds=180)
        if (self.workspace.root / "package.json").exists():
            return self.workspace.run(["npm", "test", "--", "--runInBand"], timeout_seconds=180)
        return ToolResult(True, "No supported test runner detected; inspection required.")
