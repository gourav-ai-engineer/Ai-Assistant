# Forge — Autonomous AI Software Engineer

Forge is a bounded autonomous software-engineering runtime that lets an AI inspect a repository, plan work, call typed tools, validate changes, recover from failures, and produce a persistent execution report.

## Project status

The deterministic Forge runtime is implemented and verified by GitHub Actions. Model-backed planning is implemented against the OpenAI Responses API as an optional provider. The public browser demo is a safe deterministic simulation and does not execute arbitrary visitor code.

> **Status:** Production-oriented reference implementation. Run the local test suite and benchmark after cloning before treating any performance number as a measured result.

## Architecture

`Task → Baseline Inspection → Planner → Tool Registry → Executor → Tests → Recovery → Diff Review → Final Report`

## Capabilities

- Natural-language engineering tasks
- Repository tree and structure analysis
- Text search and safe file reads/writes
- Git status, diff, and guarded commits
- Test execution
- Bounded multi-round planning and recovery
- Persistent task/run state
- Approval-gated mutations
- Workspace path traversal protection
- Credential filtering for subprocesses
- JSON execution reports
- Optional OpenAI model planning
- Docker/Compose support
- CI verification

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

Forge includes a reproducible benchmark under `benchmarks/`:

```bash
python benchmarks/run_benchmark.py
python benchmarks/run_benchmark.py --json > benchmark-result.json
```

It measures deterministic execution success, unauthorized write/commit rejection, workspace path-boundary enforcement, credential filtering, and median runtime. The benchmark intentionally does **not** invent model-quality numbers.

Only put benchmark percentages, latency numbers, or case counts on a resume after actually running the benchmark and retaining its result. This makes the claims reproducible and defensible in interviews.

## Security

Forge treats repository content and tool output as untrusted data. All paths are resolved against the selected workspace, writes require an explicit gate, commits are guarded, and common credentials are stripped from child-process environments.

See `SECURITY.md` and `docs/OPERATOR_RUNBOOK.md` for operating boundaries.

## Reference implementation

The architecture was informed by publicly available autonomous coding-agent patterns, including `sirhafizho/e2e-ai-sandbox`. Inspiration and license information are recorded in `docs/REFERENCES.md`; this repository is an independent implementation.

## Demo

Open `demo/index.html` for a portfolio-friendly deterministic workflow walkthrough. It is intentionally separate from the authoritative Python runtime.
