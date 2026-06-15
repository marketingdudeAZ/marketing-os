"""Tool definitions an agent can be given. Each wraps a read-only or write capability.

Keep write tools (budget changes) OUT of any agent that runs without a human approval gate.
The recommendation agent gets read tools only; execution happens via core.approvals after a
human clicks. See CLAUDE.md.
"""
from __future__ import annotations

from agents.base_agent import Tool
from core import attribution
from integrations import google_ads, pms


def read_tours_tool() -> Tool:
    return Tool(
        name="read_tours",
        description="Read tour events for a property over a date range.",
        input_schema={
            "type": "object",
            "properties": {
                "property_id": {"type": "string"},
                "start": {"type": "string", "description": "YYYY-MM-DD"},
                "end": {"type": "string", "description": "YYYY-MM-DD"},
            },
            "required": ["property_id", "start", "end"],
        },
        handler=lambda i: pms.get_tours(i["property_id"], i["start"], i["end"]),
    )


def read_spend_tool() -> Tool:
    return Tool(
        name="read_spend",
        description="Read daily ad spend for a property and channel over a date range.",
        input_schema={
            "type": "object",
            "properties": {
                "property_id": {"type": "string"},
                "channel": {"type": "string"},
                "start": {"type": "string"},
                "end": {"type": "string"},
            },
            "required": ["property_id", "channel", "start", "end"],
        },
        handler=lambda i: google_ads.get_spend(
            i["property_id"], i["channel"], i["start"], i["end"]
        ),
    )


def incremental_tours_tool() -> Tool:
    return Tool(
        name="incremental_tours",
        description="Given baseline and observed tours, compute incremental tours above baseline.",
        input_schema={
            "type": "object",
            "properties": {
                "baseline_per_week": {"type": "number"},
                "observed_tours": {"type": "integer"},
                "window_days": {"type": "integer"},
            },
            "required": ["baseline_per_week", "observed_tours", "window_days"],
        },
        handler=lambda i: {
            "incremental": attribution.incremental_tours(
                i["baseline_per_week"], i["observed_tours"], i["window_days"]
            )
        },
    )


# Read-only bundle for the recommendation agent.
READ_TOOLS = [read_tours_tool, read_spend_tool, incremental_tours_tool]
