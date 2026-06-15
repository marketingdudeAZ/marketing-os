# marketing-os

An outcome-oriented marketing OS for multifamily. Pulls a property's funnel data,
recommends a marketing move, and (with one-click approval and a full audit trail)
executes it. The unit that matters is the **tour** — the last funnel stage marketing
controls — measured as **incremental tours above a baseline**.

> **Status:** clean-room prototype. Personal time, personal accounts, no company data.
> See `docs/design.md` for the strategy and `CLAUDE.md` for the build brief.

## The shape

- **A — data pipe** (substrate): read tours + ad spend, live, into one view.
- **B — approve-to-execute** (the 90-day wedge): recommend a paid-search budget move,
  buyer approves one click, it executes via the Google Ads API, audit-trailed.
- **C — outcome agency** (later): run the whole funnel as a service, billed on tours.

Build B. A is its substrate. C is what B becomes. Do not build all three at once.

## Stack

Python · Supabase (Postgres) · Anthropic API · Railway (cron + webhooks) · Google Ads API · a PMS read integration.

## Layout

```
agents/         generic agent framework (recommendation, synthesis)
integrations/   pms.py (tours, read) · google_ads.py (budget, write)
core/           attribution.py (baseline + incremental tours) · approvals.py (gate + audit)
db/             schema.sql (properties, tours, recommendations, approvals, audit_log)
docs/           design.md (the strategy)
```

## Before any real build — three go/no-go gates

This prototype runs on synthetic/personal test data. A real pilot does not start until,
on one property, you have: (1) PMS tour-data access, (2) Google Ads write access without an
agency-account migration, and (3) tour data that reconciles against the CRM/calendar. If any
fails, stop. See `CLAUDE.md`.
