-- marketing-os schema (Supabase / Postgres)
-- Minimal, OS-scoped. Run in the Supabase SQL editor of YOUR OWN personal project.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- A managed property (PMS-agnostic; provider noted but not assumed).
CREATE TABLE properties (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  pms_provider TEXT,                 -- 'yardi' | 'realpage' | 'entrata' | 'synthetic'
  pms_external_id TEXT,              -- the property's id in the PMS
  market TEXT,
  -- Frozen at pilot agreement signing (see CLAUDE.md > Measurement)
  baseline_tours_per_week NUMERIC,
  baseline_frozen_at TIMESTAMPTZ,
  attribution_window_days INTEGER DEFAULT 21,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tour events pulled from the PMS. The unit we measure and bill on.
CREATE TABLE tours (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  property_id UUID REFERENCES properties(id) ON DELETE CASCADE,
  occurred_on DATE NOT NULL,
  source TEXT,                       -- channel/source if known
  pms_event_id TEXT,                 -- for dedupe against the PMS
  reconciled BOOLEAN DEFAULT FALSE,  -- verified against CRM/calendar (fidelity gate)
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (property_id, pms_event_id)
);

-- Daily ad spend by channel (Google Ads first).
CREATE TABLE ad_spend (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  property_id UUID REFERENCES properties(id) ON DELETE CASCADE,
  channel TEXT NOT NULL,             -- 'google_search' for B
  spend_date DATE NOT NULL,
  amount_cents INTEGER NOT NULL,
  external_account_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (property_id, channel, spend_date)
);

-- A recommended move (three ranked spend options) produced by the recommendation agent.
CREATE TABLE recommendations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  property_id UUID REFERENCES properties(id) ON DELETE CASCADE,
  channel TEXT NOT NULL,
  rationale TEXT,
  options JSONB NOT NULL,            -- [{level:'low'|'mid'|'high', new_budget_cents, projected_tour_delta}]
  status TEXT DEFAULT 'pending',     -- 'pending' | 'approved' | 'rejected' | 'executed'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- The governed approval. One per executed recommendation.
CREATE TABLE approvals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  recommendation_id UUID REFERENCES recommendations(id) ON DELETE CASCADE,
  approved_by TEXT NOT NULL,         -- who clicked (the buyer)
  chosen_level TEXT NOT NULL,        -- 'low' | 'mid' | 'high'
  approved_at TIMESTAMPTZ DEFAULT NOW(),
  executed_at TIMESTAMPTZ,
  execution_result JSONB             -- what the Ads API actually did (or the error)
);

-- Immutable audit trail. Append-only; every read/recommend/approve/execute lands here.
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  property_id UUID REFERENCES properties(id),
  actor TEXT NOT NULL,               -- 'agent:recommender' | 'user:<email>' | 'system'
  action TEXT NOT NULL,              -- 'read_tours' | 'recommend' | 'approve' | 'execute' | 'rollback'
  detail JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
