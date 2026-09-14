# Forge — Autonomous AI Software Engineer

Forge is a bounded autonomous software-engineering runtime that lets an AI inspect a repository, plan work, call typed tools, validate changes, recover from failures, and produce a persistent execution report.

> **Portfolio signal:** Forge is being built as a miniature autonomous software engineer — moving beyond prompt-to-code generation toward **inspect → plan → edit → validate → recover → review**, with explicit safety boundaries and reproducible evaluation.

## Project status

The deterministic runtime is implemented and verified by the local test suite and CI. Model-backed planning is available through the optional OpenAI Responses API provider. A hardened Docker sandbox runner is now available for mutation-enabled validation, with network isolation, dropped Linux capabilities, no-new-privileges, read-only container root, process/memory/CPU limits, and an ephemeral container lifecycle.

The public browser demo is a safe deterministic product walkthrough; it does not execute arbitrary visitor code.

> **Status:** Production-oriented reference implementation. Run the local test suite and benchmarks after cloning before treating any performance number as a measured result.

## Architecture

```text
Task / GitHub Issue
        ↓
Repository Inspection
        ↓
Planner
        ↓
Typed Tool Registry
        ↓
Bounded Executor
        ↓
Sandboxed Validation
        ↓
Failure / Recovery Loop
        ↓
Diff Review
        ↓
Persistent Evidence
```

## Core capabilities

- Natural-language engineering tasks
- Repository tree and structure analysis
- Safe file reads/writes with explicit approval gates
- Text search and workspace path-boundary enforcement
- Git status, diff, and guarded commits
- Bounded multi-round planning and recovery
- Failure-aware validation loop
- Hardened Docker sandbox for mutation-enabled test execution
- Network-disabled sandbox execution by default
- CPU, memory, process, and timeout limits
- Credential filtering for child processes
- Persistent JSON task/run state under `.forge/runs`
- JSON execution reports suitable for evaluation pipelines
- Optional OpenAI model planning
- Docker/Compose support
- CI verification

## Safety model

Forge separates **inspection**, **mutation**, and **validation**. Mutating tools require explicit authorization. When `--sandbox` is enabled for an authorized agent run, validation is executed inside a disposable Docker container rather than directly on the host.

The sandbox applies:

- `--network=none`
- `--cap-drop=ALL`
- `no-new-privileges`
- read-only container root filesystem
- PID, memory, and CPU limits
- isolated temporary filesystem
- controlled repository bind mount
- command execution without a shell

The sandbox image is configurable with `FORGE_SANDBOX_IMAGE`. For production deployments, use a purpose-built image containing the target repository's dependencies; stronger isolation such as gVisor or Firecracker is an advanced hardening path documented in `docs/PRD_ALIGNMENT.md`.

## Run Forge locally

```bash
python -m pip install -e ".[dev]"
python forge_cli.py "Inspect this repository and run its tests" --repo . --json
```

Model-backed mode:

```bash
python -m pip install -e ".[openai,dev]"
# PowerShell
$env:OPENAI_API_KEY = "..."
python forge_cli.py "Inspect the repository, diagnose the failing test, and propose a minimal fix" --repo ./sample-repo --json
```

For mutation tasks, explicitly add `--allow-writes`. The default is read-only.

For mutation-enabled validation in the hardened runner:

```bash
python forge_cli.py "Fix the failing test and validate the change" --repo ./sample-repo --allow-writes --sandbox --json
```

`--sandbox` requires Docker and is intentionally explicit so developers do not mistake the normal read-only local smoke test for isolated execution.

The default model is `gpt-5.6-luna`; override it with `FORGE_MODEL`.

## HTTP API

```bash
python forge_cli.py --serve --repo . --port 8787
```

The HTTP surface is intentionally read-only. Mutating operations remain in the CLI/runtime and require explicit authorization.

## Testing

```bash
pytest -q
ruff check forge tests benchmarks forge_cli.py
```

GitHub Actions compiles the package, runs the test suite, executes the Forge offline smoke test, runs the deterministic runtime benchmark, and runs the existing AI Assistant smoke test.

## Benchmark & measurable evidence

Forge includes reproducible benchmarks under `benchmarks/` covering:

- offline execution success
- unauthorized write rejection
- unauthorized Git commit rejection
- workspace path-boundary enforcement
- credential filtering
- deterministic autonomous recovery behavior
- final validation after a repair cycle

The runtime safety benchmark has been verified at **5/5 cases passed (100%)** in the current development cycle. Runtime numbers should only be quoted from retained benchmark output because they depend on the machine and environment.

The benchmarks intentionally avoid fabricating LLM-quality metrics. Model performance should be measured separately on a curated issue suite or SWE-bench-style dataset.

## PRD alignment

The attached enterprise PRD is tracked in `docs/PRD_ALIGNMENT.md`, separating implemented capabilities from the next engineering milestones. The current implementation prioritizes the highest-signal primitives: bounded tool use, approval gates, workspace security, persistent run state, recovery, deterministic evaluation, and sandboxed validation.

## Resume / achievement positioning

### Safe achievement claim today

> **Building Forge, an autonomous AI software-engineering runtime that can inspect repositories, plan and execute typed code changes, validate patches, recover from test failures, and produce auditable execution reports with explicit safety controls.**

### Stronger claim after model-backed sandbox runs are benchmarked

> **Engineering Forge, a verification-first autonomous coding agent that turns software tasks into bounded inspect → plan → patch → sandbox-test → failure-recovery loops, with reproducible safety and recovery benchmarks.**

Do not claim full GitHub issue-to-PR autonomy, SWE-bench resolution rates, or production-grade sandbox isolation until those features are actually implemented and benchmarked.

## Reference implementation

The architecture was informed by publicly available autonomous coding-agent patterns, including `sirhafizho/e2e-ai-sandbox`. Inspiration and license information are recorded in `docs/REFERENCES.md`; this repository is an independent implementation.

## Demo

Open `demo/index.html` for a portfolio-friendly deterministic workflow walkthrough. It is intentionally separate from the authoritative Python runtime.
