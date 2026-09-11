# Forge — Autonomous Software Engineer

Forge is the flagship autonomous coding-agent project in this portfolio. It turns a natural-language software task into a controlled engineering workflow: inspect a repository, plan work, use typed tools, run validation, and return an auditable run report.

> This repository began as `Ai-Assistant`; the current codebase is being evolved into Forge rather than discarded. The historical coding-practice workflow remains available while the new `forge/` runtime becomes the primary engineering system.

## What is implemented

- Explicit task contract and structured run reports
- Repository-scoped workspace with path-traversal protection
- Typed tool registry for repository listing, file reads/writes, Git status/diff, and tests
- Shell execution with `shell=False` and credential stripping
- Write approval gate with safe read-only default
- Deterministic offline planner for reproducible local development
- Optional OpenAI Responses API planner loaded only when `OPENAI_API_KEY` is present
- Strict JSON planner output validation before tool execution
- Unit tests covering workspace isolation, approvals, planner parsing, and end-to-end smoke execution
- Architecture, security, references, and contribution documentation

## Quick start

```bash
python -m pytest -q
python -m forge_cli --repo . --json
python -m forge_cli "Inspect the repository and run its tests" --repo . --json
```

Model-backed planning is optional:

```bash
pip install -e '.[openai]'
set OPENAI_API_KEY=...
python -m forge_cli "Find and fix the failing tests" --repo . --allow-writes --json
```

Never commit credentials. Use a dedicated sandbox/container before giving Forge access to untrusted repositories.

## Architecture

`User Task → Task Contract → Planner → Tool Registry → Workspace → Validation → RunReport`

The production roadmap extends this core to Repository Analyzer, Tool Selector, Executor, Test Runner, Debugger, Reviewer, Finalizer, Docker isolation, persistent task state, GitHub integration, human approval checkpoints, and observability.

## Engineering quality

```text
forge/                  core runtime
src/                    historical coding-practice modules
scripts/                operational helpers (as added)
tests/                  automated tests
docs/                   architecture + research notes
.github/workflows/      CI
```

CI compiles the repository and runs the complete test suite plus the existing coding-assistant smoke test.

## References

See `docs/REFERENCES.md` for the public projects and official documentation used as architectural inspiration. No reference implementation is copied verbatim.
