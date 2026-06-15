# marketing-os — Build Brief

## What we are building

An outcome-oriented marketing OS for multifamily. It pulls a property's funnel data, tells
the operator what marketing move to make, and on one-click approval executes it with a full
audit trail. The unit of value is the **tour** — the last funnel stage marketing controls —
measured as **incremental tours above an agreed baseline**.

This replaces two things multifamily marketing managers do today: screenshotting agency
reports into PowerPoint, and pasting those screenshots into ChatGPT for advice they then
can't act on without a week of email approvals.

## Who it's for (this drives everything)

- **Economic buyer:** the regional VP of Operations / owner-operator. Measured on NOI, tours,
  cost-per-lease. Signs the check. Sell to this person.
- **Daily user:** the Marketing Manager. Owns lead → prospect → tour. Uses the tool, but is
  NOT the buyer. Never pitch the user a tool framed as replacing them.
- The two are structurally misaligned: ops cares about NOI, marketing cares about looking
  smart. The product wins by reframing spend from "tell a smart story" to "prove and drive
  tours."

## The shape: A → B → C (build B; do not build all three at once)

- **A — data pipe (substrate).** Read tours (PMS) + ad spend (Google Ads), live, into one
  view. You need this regardless. The narrative on top is commoditized; the pipe is the value.
- **B — approve-to-execute (the 90-day wedge).** Recommend a paid-search budget move (three
  spend levels, each with a projected tour delta), buyer approves one, it executes via the
  Google Ads API, audit-trailed. Billed on incremental tours.
- **C — outcome agency (later).** Run the whole funnel (creative, ILS, social) as a service,
  paid per incremental tour. This is what B's engine becomes once the economics are proven
  across 5–10 properties. Not the launch.

## Measurement (the load-bearing mechanic)

- **Baseline:** the property's trailing 8-week tour rate, same-season prior-year adjusted,
  frozen at agreement signing. Simplest defensible method for one property. No seasonality
  model or holdout at n=1.
- **Attribution window:** default 21 days post-change (14–30 negotiable, fixed at signing).
- **Tour-data fidelity:** PMS tours are often hand-logged and under-recorded. Reconcile PMS
  tour counts against CRM/calendar before trusting them.
- Bill on the *incremental* unit, not raw cost-per-tour (which buyers already track).

## Three go/no-go gates (before any real-property pilot)

This repo runs on synthetic/personal test data. A funded pilot does NOT start until, on one
property, you have all three:
1. PMS tour-data access (or owner-operator-authorized access).
2. Google Ads write access WITHOUT migrating off the agency's account.
3. Tour data that actually reconciles against the CRM/calendar.
If any fails, do not build the pilot. The whole arc is downstream of these.

## Clean-room discipline

Personal time, personal machine, personal API keys, no company data, ever. This keeps the IP
unambiguously yours and preserves the option to commercialize. Build PMS-agnostic; do not
hardcode any one company's quirks.

## Stack

Python · Supabase (Postgres) · Anthropic API (use `claude-opus-4-8` for judgment-heavy
agents, `claude-sonnet-4-6` for routine ones) · Railway (cron + webhooks) · Google Ads API ·
a PMS read integration (provider TBD: Yardi / RealPage / Entrata).

## Build order

1. `db/schema.sql` — properties, tours, ad_spend, recommendations, approvals, audit_log.
2. `integrations/pms.py` — read tours for a property (stub against synthetic data first).
3. `integrations/google_ads.py` — read spend; write budget (sandbox account first).
4. `core/attribution.py` — compute baseline + incremental tours.
5. `agents/` — the recommendation agent that turns the data into three ranked budget options.
6. `core/approvals.py` — the approval gate + immutable audit log.
7. A thin approval UI (later — CLI or simple web first).

Build A's read path end to end on synthetic data before touching any write path.

## The agent-run company (goal: ~0 payroll)

The end-state (C) is a multifamily marketing company run almost entirely by AI agents. The
org is modeled in `agents/org.py` as a Manager → Doer hierarchy per department, plus a Chief
of Staff that reports to the human founder.

**Activation policy — this is the discipline that keeps it from becoming theater:**
- Scaffold the whole org now so it scales, but only ACTIVATE an agent when its function has
  real work. Pre-revenue, that's just the Delivery loop (Recommender + Attribution/Reporting)
  and the Chief of Staff. Growth, CS, Finance, Support stay dormant with a written
  `activate_when` trigger. A Finance agent reconciling $0 is theater.
- "0 payroll" means no employees. It does NOT mean no humans in any loop. Two humans stay by
  design: (1) the CUSTOMER approving each budget change — that governance gate is the
  product's trust feature, the thing that makes outcome billing sellable, not headcount to
  remove; (2) the founder's own judgment, contracts, and the upside/sponsor negotiation.
- Run `python -m agents.org` to see what's on vs. waiting and why.

Two distinct agentic layers, don't conflate them: the PRODUCT loop (recommend → approve →
execute, per property) and the COMPANY back-office (growth, CS, finance...). The product loop
is the moat and ships first. The back-office agents are how the company scales to ~0 payroll
later, not what you build before you have a customer.
