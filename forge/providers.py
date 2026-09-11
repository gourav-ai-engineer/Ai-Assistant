from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

from .planner import JSONPlanner, SYSTEM_PROMPT
from .types import ForgeTask, ToolCall


@dataclass(frozen=True)
class OpenAIPlanner:
    """Optional model-backed planner using the OpenAI Responses API.

    The API key is read only from the process environment and is never passed
    into the repository workspace.
    """

    model: str = "gpt-5.6-mini"

    def plan(self, task: ForgeTask, context: str) -> tuple[ToolCall, ...]:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install the optional 'openai' dependency to use model planning") from exc

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        user = (
            f"Task: {task.request}\nWorkspace snapshot:\n{context[-30_000:]}\n"
            "Return only the required JSON object."
        )
        response = client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=user,
        )
        raw = response.output_text
        return JSONPlanner().parse(raw)


def provider_from_env() -> OpenAIPlanner | None:
    if os.getenv("OPENAI_API_KEY"):
        return OpenAIPlanner(model=os.getenv("FORGE_MODEL", "gpt-5.6-mini"))
    return None
