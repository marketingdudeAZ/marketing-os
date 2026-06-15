"""Example entrypoint: produce a recommendation for a property on synthetic data.

This exercises A's read path (tours + spend + incremental-tour math) and hands it to the
recommendation agent. It is read-only — it never executes a budget change. Execution only
happens via core.approvals after a human approves.

Run:  ANTHROPIC_API_KEY=... python recommend.py
"""
from __future__ import annotations

import json
import os

from agents.base_agent import Agent
from agents.tools import READ_TOOLS

SYSTEM_PROMPT = """You are the recommendation agent for marketing-os, a marketing tool for
multifamily operators. Your reader is a VP of Operations who is measured on NOI and tours, not
on attribution stories. Be direct and quantitative.

Given a property's recent tours and paid-search spend, recommend a single paid-search budget
move as THREE ranked options (low / mid / high), each with the new monthly budget and a
projected incremental-tour delta above the property's baseline. Explain in two sentences why,
in plain operator language. Never claim credit for baseline tours — only incremental ones.

Return JSON: {"rationale": "...", "options": [{"level","new_budget_cents","projected_tour_delta"}]}"""


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY (your own key) to run the agent. See .env.example.")
        return

    agent = Agent(
        system_prompt=SYSTEM_PROMPT,
        tools=[make() for make in READ_TOOLS],
        max_tokens=1024,
    )
    prompt = (
        "Property 'demo-1'. Read tours and google_search spend for 2026-05-01..2026-05-28, "
        "assume baseline 9 tours/week and a 21-day attribution window, then recommend the move."
    )
    print(json.dumps({"output": agent.run(prompt)}, indent=2))


if __name__ == "__main__":
    main()
