from __future__ import annotations

import logging

import requests

from .problems import Problem

logger = logging.getLogger(__name__)


def generate_with_llm(problem: Problem, *, api_key: str, base_url: str, model: str) -> str:
    """Generate Python code using an OpenAI-compatible chat-completions endpoint."""
    prompt = (
        "Return only valid Python code. Solve this coding problem with a function named solution.\n\n"
        f"Problem: {problem.name}\nStatement: {problem.statement}\nHint: {problem.hint}\n"
        f"Starter signature:\n{problem.starter_code}"
    )
    response = requests.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "temperature": 0.1,
            "messages": [
                {"role": "system", "content": "You are a careful competitive programming assistant."},
                {"role": "user", "content": prompt},
            ],
        },
        timeout=45,
    )
    response.raise_for_status()
    payload = response.json()
    content = payload["choices"][0]["message"]["content"].strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return content + "\n"
