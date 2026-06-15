"""Baseline + incremental-tour math.

This is the load-bearing mechanic of the whole business: you bill on tours DRIVEN above a
frozen baseline, not raw tour count. Keep it simple and defensible at n=1 (one property).
Seasonality models and holdout designs are deferred to the multi-property stage (C).
"""
from __future__ import annotations


def expected_baseline_tours(baseline_per_week: float, window_days: int) -> float:
    """Tours you'd have expected with no change, over the attribution window."""
    if baseline_per_week < 0 or window_days <= 0:
        raise ValueError("baseline_per_week must be >= 0 and window_days > 0")
    return baseline_per_week * (window_days / 7.0)


def incremental_tours(baseline_per_week: float, observed_tours: int, window_days: int) -> float:
    """Observed tours minus the baseline expectation over the window. Floored at 0.

    This is the unit you invoice on. A negative result means the move did not beat baseline;
    you bill nothing, you do not claw back.
    """
    expected = expected_baseline_tours(baseline_per_week, window_days)
    return max(0.0, observed_tours - expected)


def projected_tour_delta(
    current_spend_cents: int,
    new_spend_cents: int,
    tours_per_dollar: float,
) -> float:
    """Naive linear projection for the three spend options shown to the buyer.

    `tours_per_dollar` is the recent marginal tour yield for the channel. Linear is a
    deliberate placeholder; replace with a fitted response curve once there's enough history.
    """
    delta_dollars = (new_spend_cents - current_spend_cents) / 100.0
    return max(0.0, delta_dollars * tours_per_dollar)
