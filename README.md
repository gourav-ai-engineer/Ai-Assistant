# Forge — Autonomous AI Software Engineer

Forge is a bounded autonomous software-engineering runtime that lets an AI inspect a repository, plan work, call typed tools, validate changes, recover from failures, and produce a persistent execution report.

## Project status

The deterministic Forge runtime is implemented and verified by GitHub Actions. Model-backed planning is implemented against the OpenAI Responses API as an optional provider. The public browser demo is a safe deterministic simulation and does not execute arbitrary visitor code.

## Architecture

`Task → Baseline Inspection → Planner → Tool Registry → Executor → Tests → Recovery → Diff Review → Final Report`

Core modules:

```text
forge/
├── analyzer.py      repository language/entry-point analysis
├── engine.py        bounded autonomous execution loop
├── planner.py       planner protocol + offline deterministic planner
├── providers.py     optional OpenAI Responses API planner
├── server.py        local read-only inspection HTTP API
├── state.py         persistent run reports
├── tools.py         typed and guarded tool registry
├── types.py         task/report/tool data models
└── workspace.py     repository boundary and safe file access
```

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

Safe offline mode:

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
ruff check forge tests forge_cli.py
```

GitHub Actions additionally compiles the Forge package and runs both a Forge offline smoke test and the existing AI Assistant smoke test.

## Security

Forge treats repository content and tool output as untrusted data. All paths are resolved against the selected workspace, writes require an explicit gate, commits are guarded, and common credentials are stripped from child-process environments.

See `SECURITY.md` and `docs/OPERATOR_RUNBOOK.md` for operating boundaries.

## Reference implementation

The architecture was informed by publicly available autonomous coding-agent patterns, including `sirhafizho/e2e-ai-sandbox`. Inspiration and license information are recorded in `docs/REFERENCES.md`; this repository is an independent implementation.

## Demo

Open `demo/index.html` for a portfolio-friendly deterministic workflow walkthrough. It is intentionally separate from the authoritative Python runtime.
