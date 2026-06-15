# Design summary

This is a condensed pointer. The full, reviewed design doc from the office-hours session lives
at:

`~/.gstack/projects/kyleshipp/kyleshipp-unknown-design-20260614-181903.md`

(Status: APPROVED. Mode: Intrapreneurship — build inside the current PMC, leveraging a
~900-property base for distribution and data access.)

## The one-paragraph version

Multifamily marketing managers can't speak to reporting, MMM, or budgeting; they use
attribution to look smart, not to drive leasing. The economic buyer is Operations (NOI), not
marketing. Sell the buyer a closed loop — live data in, a governed approve-to-execute trigger
out — billed on incremental tours. The recommendation itself is commoditized (users already
paste reports into ChatGPT); the moat is closing the loop plus outcome-aligned pricing plus
being PMS-agnostic.

## Open strategic items (not code)

- Negotiate personal upside (equity / profit share / NOI bonus / IP co-ownership /
  external-commercialization rights) BEFORE building on company resources. Leverage is highest
  now.
- Lock an executive sponsor (one level above the champion, to survive a reorg) and a funded
  pilot cohort with a matched control cohort.
- One hour with an employment lawyer on IP-assignment / non-compete clauses.
- A clean-room working prototype (this repo) strengthens all of the above.

## Salvaged from the shelved `vero` project

Vero (a multifamily vendor review directory) is shelved as a product. Reused here: the
agentic framework pattern, Supabase/Railway/Anthropic infra patterns, and the
practitioner-vs-leadership role logic (which mirrors the buyer-vs-user split). Dropped: the
entire reviews/directory/grading marketplace.
