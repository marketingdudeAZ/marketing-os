"""The governance layer: approval gate + immutable audit log.

Nothing executes without passing through here. A human (the buyer) approves a specific option
on a recommendation; we mint an approval token, write an audit row, then — and only then — let
the execution path mutate a budget. Every step is logged.
"""
from __future__ import annotations

import uuid
from typing import Any


def _audit(supabase, property_id: str, actor: str, action: str, detail: dict) -> None:
    supabase.table("audit_log").insert({
        "property_id": property_id,
        "actor": actor,
        "action": action,
        "detail": detail,
    }).execute()


def record_approval(
    supabase,
    *,
    recommendation_id: str,
    property_id: str,
    approved_by: str,
    chosen_level: str,
) -> str:
    """Persist a human approval and return an approval token for the execution path.

    The token is the only thing integrations.google_ads.set_campaign_budget will accept.
    """
    if chosen_level not in {"low", "mid", "high"}:
        raise ValueError("chosen_level must be one of: low, mid, high")

    token = f"appr_{uuid.uuid4().hex}"
    supabase.table("approvals").insert({
        "recommendation_id": recommendation_id,
        "approved_by": approved_by,
        "chosen_level": chosen_level,
    }).execute()
    supabase.table("recommendations").update(
        {"status": "approved"}
    ).eq("id", recommendation_id).execute()
    _audit(supabase, property_id, f"user:{approved_by}", "approve", {
        "recommendation_id": recommendation_id,
        "chosen_level": chosen_level,
        "token": token,
    })
    return token


def execute_approved(
    supabase,
    *,
    property_id: str,
    recommendation_id: str,
    approval_token: str,
    execute_fn,
) -> dict[str, Any]:
    """Run the (already-approved) change via execute_fn, recording the result.

    execute_fn must call integrations.google_ads.set_campaign_budget with the token. Any error
    is captured to the audit log rather than swallowed.
    """
    try:
        result = execute_fn(approval_token)
        status, detail = "executed", {"result": result}
    except Exception as e:  # noqa: BLE001 — we want to log every failure mode
        status, detail = "failed", {"error": repr(e)}

    supabase.table("recommendations").update({"status": status}).eq(
        "id", recommendation_id
    ).execute()
    _audit(supabase, property_id, "system", "execute", {
        "recommendation_id": recommendation_id, "status": status, **detail,
    })
    return {"status": status, **detail}
