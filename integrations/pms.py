"""PMS read integration (tours).

PMS-agnostic by design. Real providers (Yardi / RealPage / Entrata) gate their APIs hard, so
the provider stays abstract until the pilot property is known and access is granted (go/no-go
gate #1). Until then, `get_tours` returns synthetic data so the read path above it can be
built and tested end to end.

DO NOT add a write path here. The PMS is a source of truth we read, never mutate.
"""
from __future__ import annotations

import os
from datetime import date, datetime, timedelta


def _synthetic_tours(property_id: str, start: str, end: str) -> list[dict]:
    """Deterministic fake tours so A's read path is testable without a real PMS."""
    d0 = datetime.strptime(start, "%Y-%m-%d").date()
    d1 = datetime.strptime(end, "%Y-%m-%d").date()
    out: list[dict] = []
    day = d0
    i = 0
    while day <= d1:
        # ~2 tours/weekday, ~1/weekend — just enough shape to exercise the math.
        n = 2 if day.weekday() < 5 else 1
        for k in range(n):
            out.append({
                "property_id": property_id,
                "occurred_on": day.isoformat(),
                "source": "synthetic",
                "pms_event_id": f"syn-{day.isoformat()}-{k}",
                "reconciled": False,
            })
            i += 1
        day += timedelta(days=1)
    return out


def get_tours(property_id: str, start: str, end: str) -> list[dict]:
    """Return tour events for a property over [start, end] (YYYY-MM-DD, inclusive).

    Routes to a real PMS client when PMS_PROVIDER is set and supported; otherwise synthetic.
    """
    provider = os.environ.get("PMS_PROVIDER", "").lower()
    if not provider or provider == "synthetic":
        return _synthetic_tours(property_id, start, end)

    # TODO: implement per-provider clients once access is granted (gate #1).
    #   yardi    -> Yardi Voyager / RentCafe API
    #   realpage -> RealPage API
    #   entrata  -> Entrata API
    raise NotImplementedError(
        f"PMS provider '{provider}' not implemented yet. "
        "Do not start a real pilot until tour-data access is confirmed (CLAUDE.md gate #1)."
    )


def reconcile_against_crm(tours: list[dict]) -> dict:
    """Fidelity gate: compare PMS tour counts to the CRM/calendar before trusting them.

    Returns a summary; flips `reconciled` only when counts agree within tolerance. Hand-logged
    PMS tours are often under-recorded — if this doesn't reconcile on the pilot property, there
    is nothing trustworthy to bill on (CLAUDE.md gate #3).
    """
    # TODO: wire to the property's CRM/calendar source of truth.
    raise NotImplementedError("CRM reconciliation pending pilot-property CRM access.")
