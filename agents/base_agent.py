"""Generic agent framework for marketing-os.

A thin wrapper over the Anthropic Messages API with a tool-use loop. Lifted from the
shelved `vero` project's pattern and stripped to the generic core. Subclass or instantiate
with a system prompt and a list of tools.

Model policy (see CLAUDE.md): claude-opus-4-8 for judgment-heavy agents, claude-sonnet-4-6
for routine ones.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Callable

from anthropic import Anthropic

DEFAULT_MODEL = "claude-sonnet-4-6"


@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict
    handler: Callable[[dict], Any]

    def spec(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }


@dataclass
class Agent:
    system_prompt: str
    tools: list[Tool] = field(default_factory=list)
    model: str = DEFAULT_MODEL
    max_tokens: int = 1024
    _client: Anthropic = field(default=None, repr=False)

    def __post_init__(self) -> None:
        self._client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def _tool(self, name: str) -> Tool:
        for t in self.tools:
            if t.name == name:
                return t
        raise KeyError(f"unknown tool: {name}")

    def run(self, user_message: str, max_turns: int = 8) -> str:
        """Run the tool loop until the model returns a final text answer."""
        messages: list[dict] = [{"role": "user", "content": user_message}]
        tool_specs = [t.spec() for t in self.tools]

        for _ in range(max_turns):
            resp = self._client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=self.system_prompt,
                tools=tool_specs,
                messages=messages,
            )
            messages.append({"role": "assistant", "content": resp.content})

            if resp.stop_reason != "tool_use":
                return "".join(b.text for b in resp.content if b.type == "text")

            results = []
            for block in resp.content:
                if block.type != "tool_use":
                    continue
                out = self._tool(block.name).handler(block.input)
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(out, default=str),
                })
            messages.append({"role": "user", "content": results})

        raise RuntimeError("agent exceeded max_turns without a final answer")
