"""Google Ads integration: read spend, and (guarded) write campaign budget.

The budget write is the ONLY mutation in the system and it is the thing that makes outcome
billing legitimate. It must never run except from core.approvals after a human has approved a
specific recommendation. The write function refuses to run without an explicit approval token.
Start against a Google Ads *sandbox/test* account (go/no-go gate #2).
"""
from __future__ import annotations

import os


def get_spend(property_id: str, channel: str, start: str, end: str) -> list[dict]:
    """Daily spend for a property+channel over [start, end]. Read-only."""
    if not os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN"):
        # Synthetic until credentials exist, so the read path is testable.
        return [{
            "property_id": property_id,
            "channel": channel,
            "spend_date": start,
            "amount_cents": 0,
            "external_account_id": "synthetic",
        }]
    # TODO: implement via google-ads client (GAQL query on the customer/campaign).
    raise NotImplementedError("Google Ads read client not implemented yet.")


def set_campaign_budget(
    *,
    customer_id: str,
    campaign_budget_id: str,
    new_amount_cents: int,
    approval_token: str,
) -> dict:
    """Set a campaign budget. THE one write path. Requires a valid approval token.

    `approval_token` must come from core.approvals.record_approval — it proves a human chose
    this change. Do not call this directly from an agent.
    """
    if not approval_token or not approval_token.startswith("appr_"):
        raise PermissionError(
            "set_campaign_budget requires a valid approval token from core.approvals. "
            "No autonomous budget changes."
        )
    if new_amount_cents <= 0:
        raise ValueError("new_amount_cents must be > 0")

    # TODO: implement the actual CampaignBudgetService mutate via the google-ads client.
    # "Rollback" = set the budget back to the prior value; already-spent money is NOT
    # recoverable (CLAUDE.md).
    raise NotImplementedError(
        "Budget write not implemented. Wire to a SANDBOX Google Ads account first (gate #2)."
    )
