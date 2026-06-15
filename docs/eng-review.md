# Engineering Review — 2026-06-14

Output of `/plan-eng-review` against the approved design doc
(`~/.gstack/projects/kyleshipp/kyleshipp-unknown-design-20260614-181903.md`).

## Headline: build is GATED

**T0 (blocks all code): settle IP + upside before writing more product code.**
Cross-model consensus (Claude review + independent outside voice): every commit
decays your negotiating leverage, and clean-room coding does not clean-room the
*business* (the value thesis is the company's ~900-property base, which likely
puts this inside a standard IP-assignment clause). One hour with an employment
lawyer + a written upside/IP/commercialization deal comes FIRST.

## Architecture decisions (folded into the plan)

- **A1** — Recommendation flow is a deterministic pipeline (fetch + compute in
  code), one LLM call only to write the rationale and rank three precomputed
  spend options. `recommend.py` currently still uses the old tool-loop — rebuild it.
- **A2** — Ground the buyer-facing tour projection in real marginal yield and
  show a range; label it an estimate when history is thin.
- **A3** — Enforce `audit_log` append-only at the DB (revoke UPDATE/DELETE). It's
  your evidence in a billing dispute; if it's editable it isn't evidence.
- **A4** — Make budget execution idempotent via an atomic single-use claim on the
  approval row (guards the metric you bill on against double-spend).

## Cross-model tensions (all accepted)

- **T1 (sequencing)** — Pause code until IP/upside settled. (See T0.)
- **T2 (measurement)** — The frozen-baseline billing unit is causally invalid and
  upward-biased (captures market/seasonal noise, floors at 0, no clawback, 21-day
  window may be shorter than the lead-to-tour lag, linear projection over-promises
  on the high option). Bill on **difference-in-differences vs a matched control
  cohort**; the schema needs a control-property concept.
- **T3 (agency)** — "Ads write access without migrating off the agency's account"
  means two writers on one account. Self-idempotency (A4) doesn't help. Add
  **live-budget reconciliation + drift detection** before each recommend/execute.

Also flagged by the outside voice: VPs won't click daily approvals while the only
daily user is the marketing manager the tool threatens (resolve the approval
delegation); and baseline-vs-window tour-reconciliation parity matters, not just
per-row flags.

## Test gap

Zero tests today; the untested code is the money math. Coverage target 100% on
`core/`. See `docs/../` test plan. pytest unit tests for attribution branches,
approvals (mocked Supabase, incl. the A4 already-consumed rejection), the Google
Ads token guard, and the PMS reader; one integration test for
approve → execute → double-execute-blocked. LLM eval deferred (A1 moved the math
out of the model).

## Implementation tasks (all code tasks gated behind T0)

- [ ] **T0 (P1, GATE, non-code)** — Lawyer hour on IP/non-compete + signed upside deal before any further code
- [ ] **T1 (P1)** — Rebuild `recommend.py` as deterministic pipeline + 1 LLM call (A1)
- [ ] **T2 (P1)** — Enforce `audit_log` append-only (revoke UPDATE/DELETE) (A3)
- [ ] **T3 (P1)** — Atomic single-use approval claim before execute (A4)
- [ ] **T4 (P1)** — Control-property + difference-in-differences billing; window/lag + saturation (T2)
- [ ] **T5 (P1)** — Live-budget reconciliation + drift detection (T3)
- [ ] **T6 (P1)** — Ground projection in real marginal yield + range (A2)
- [ ] **T7 (P1)** — pytest suite + approve→execute→double-block integration test
- [ ] **T8 (P2)** — Move `agents/org.py` → `docs/company-vision.md` (scope reduction)
- [ ] **T9 (P2)** — Resolve daily-approval adoption (VP won't click daily)
- [ ] **T10 (P2)** — Require baseline-vs-window tour-reconciliation parity
- [ ] **T11 (P3)** — ruff + mypy; batch-insert PMS sync

VERDICT: Eng reviewed, NOT cleared to implement — resume the B-loop build only
after T0 (IP/upside) closes.
