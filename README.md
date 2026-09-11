# AI Coding Assistant

A small, reproducible autonomous coding-practice assistant. It selects a coding problem, shows a hint, optionally opens coding platforms, generates a trusted reference solution, validates it against test cases, stores progress, and can optionally publish the generated solution to GitHub.

## Architecture

`Problem Bank → Generator → Validator → Tracker → GitHub Publisher`

An optional OpenAI-compatible LLM can generate a candidate solution for review. LLM code is saved for inspection and is **not executed automatically**.

## Quick start

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py --once --problem two-sum
```

The command should print a PASS result and create a generated solution plus `data/progress.jsonl`.

Run all tests:

```bash
pytest -q
```

Run continuously (example: every hour):

```bash
python main.py --interval 3600
```

The previous implementation ran its loop immediately on import and used a 5-second schedule while sleeping for 60 seconds. The v2 CLI fixes both behaviors and requires an explicit command entry point.

## GitHub publishing

Publishing is disabled by default. Copy `.env.example` to `.env` and set:

```text
AI_ASSISTANT_AUTO_PUBLISH=true
GITHUB_REPO=gourav-ai-engineer/Ai-Assistant
GITHUB_TOKEN=your_token
GITHUB_BRANCH=main
```

The token needs permission to create repository contents. The application uses the GitHub Contents API rather than shelling out to `git add/commit/push`, which makes failures visible and avoids arbitrary shell command execution.

## Optional LLM generation

Set `OPENAI_API_KEY` and the optional `OPENAI_BASE_URL` / `OPENAI_MODEL` values. The assistant will save the model-generated candidate under `generated/` while continuing to use the trusted built-in reference implementation as the validation oracle.

## Safe defaults

`AI_ASSISTANT_OPEN_PLATFORMS=false` and `AI_ASSISTANT_AUTO_PUBLISH=false` by default. Nothing opens in your browser and nothing is pushed remotely unless you explicitly enable it.

## Project structure

```text
.
├── main.py
├── requirements.txt
├── .env.example
├── src/
│   ├── automation.py
│   ├── config.py
│   ├── github_worker.py
│   ├── llm.py
│   ├── notifier.py
│   ├── problems.py
│   ├── service.py
│   ├── solver.py
│   ├── tracker.py
│   └── validator.py
├── tests/
├── data/
└── generated/
```

## Verification

GitHub Actions runs dependency installation, Python compilation, the complete pytest suite, and a `two-sum` end-to-end smoke test on pushes and pull requests.
