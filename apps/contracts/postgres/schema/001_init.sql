CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS camera_groups (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  name TEXT NOT NULL,
  description TEXT,
  camera_ids TEXT[] NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_camera_groups_name ON camera_groups (name);
CREATE INDEX IF NOT EXISTS idx_camera_groups_camera_ids ON camera_groups USING GIN (camera_ids);

CREATE TABLE IF NOT EXISTS saved_prompts (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  name TEXT NOT NULL,
  description TEXT,
  prompt_text TEXT NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_saved_prompts_enabled ON saved_prompts (enabled);
CREATE INDEX IF NOT EXISTS idx_saved_prompts_created_at ON saved_prompts (created_at DESC);

CREATE TABLE IF NOT EXISTS prompt_bindings (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  camera_group_id TEXT NOT NULL REFERENCES camera_groups(id) ON DELETE CASCADE,
  prompt_id TEXT NOT NULL REFERENCES saved_prompts(id) ON DELETE CASCADE,
  enabled BOOLEAN NOT NULL DEFAULT true,
  last_run_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (camera_group_id, prompt_id)
);

CREATE INDEX IF NOT EXISTS idx_prompt_bindings_camera_group_id ON prompt_bindings (camera_group_id);
CREATE INDEX IF NOT EXISTS idx_prompt_bindings_prompt_id ON prompt_bindings (prompt_id);
CREATE INDEX IF NOT EXISTS idx_prompt_bindings_enabled ON prompt_bindings (enabled);

CREATE TABLE IF NOT EXISTS operations (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  prompt_id TEXT NOT NULL REFERENCES saved_prompts(id) ON DELETE RESTRICT,
  camera_group_id TEXT NOT NULL REFERENCES camera_groups(id) ON DELETE RESTRICT,
  prompt_binding_id TEXT REFERENCES prompt_bindings(id) ON DELETE SET NULL,
  trigger TEXT NOT NULL DEFAULT 'manual' CHECK (trigger IN ('manual', 'scheduled')),
  status TEXT NOT NULL DEFAULT 'queued' CHECK (status IN ('queued', 'running', 'completed', 'failed', 'cancelled')),
  total_cameras INTEGER NOT NULL DEFAULT 0,
  processed_cameras INTEGER NOT NULL DEFAULT 0,
  matched_cameras INTEGER NOT NULL DEFAULT 0,
  estimated_gemini_calls INTEGER,
  estimated_token_count INTEGER,
  estimated_cost NUMERIC(12, 6),
  actual_gemini_calls INTEGER,
  actual_cost NUMERIC(12, 6),
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_operations_status ON operations (status);
CREATE INDEX IF NOT EXISTS idx_operations_prompt_id ON operations (prompt_id);
CREATE INDEX IF NOT EXISTS idx_operations_camera_group_id ON operations (camera_group_id);
CREATE INDEX IF NOT EXISTS idx_operations_prompt_binding_id ON operations (prompt_binding_id);
CREATE INDEX IF NOT EXISTS idx_operations_created_at ON operations (created_at DESC);

CREATE TABLE IF NOT EXISTS camera_frame_refs (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  camera_id TEXT NOT NULL,
  frame_id TEXT NOT NULL,
  snapshot_id TEXT,
  frame_url TEXT NOT NULL,
  sequence_number BIGINT,
  captured_at TIMESTAMPTZ NOT NULL,
  mime_type TEXT NOT NULL DEFAULT 'image/jpeg',
  width INTEGER,
  height INTEGER,
  expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (camera_id, frame_id)
);

CREATE INDEX IF NOT EXISTS idx_camera_frame_refs_camera_id ON camera_frame_refs (camera_id);
CREATE INDEX IF NOT EXISTS idx_camera_frame_refs_captured_at ON camera_frame_refs (captured_at DESC);
CREATE INDEX IF NOT EXISTS idx_camera_frame_refs_camera_latest ON camera_frame_refs (camera_id, captured_at DESC);
CREATE INDEX IF NOT EXISTS idx_camera_frame_refs_frame_url ON camera_frame_refs (frame_url);

CREATE TABLE IF NOT EXISTS operation_results (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  operation_id TEXT NOT NULL REFERENCES operations(id) ON DELETE CASCADE,
  camera_id TEXT NOT NULL,
  camera_group_id TEXT REFERENCES camera_groups(id) ON DELETE SET NULL,
  prompt_id TEXT REFERENCES saved_prompts(id) ON DELETE SET NULL,
  frame_ref_id TEXT NOT NULL REFERENCES camera_frame_refs(id) ON DELETE RESTRICT,
  frame_url TEXT NOT NULL,
  include BOOLEAN NOT NULL DEFAULT false,
  prompt_match_score NUMERIC(5, 2) NOT NULL DEFAULT 0 CHECK (prompt_match_score >= 0 AND prompt_match_score <= 100),
  operator_priority_score NUMERIC(5, 2) NOT NULL DEFAULT 0 CHECK (operator_priority_score >= 0 AND operator_priority_score <= 100),
  recommended_action TEXT NOT NULL,
  reason TEXT NOT NULL,
  raw_model_json JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (operation_id, camera_id, frame_ref_id)
);

CREATE INDEX IF NOT EXISTS idx_operation_results_operation_id ON operation_results (operation_id);
CREATE INDEX IF NOT EXISTS idx_operation_results_camera_id ON operation_results (camera_id);
CREATE INDEX IF NOT EXISTS idx_operation_results_prompt_id ON operation_results (prompt_id);
CREATE INDEX IF NOT EXISTS idx_operation_results_include ON operation_results (include);
CREATE INDEX IF NOT EXISTS idx_operation_results_prompt_match_score ON operation_results (prompt_match_score DESC);
CREATE INDEX IF NOT EXISTS idx_operation_results_operator_priority_score ON operation_results (operator_priority_score DESC);

CREATE TABLE IF NOT EXISTS operation_frame_refs (
  operation_id TEXT NOT NULL REFERENCES operations(id) ON DELETE CASCADE,
  frame_ref_id TEXT NOT NULL REFERENCES camera_frame_refs(id) ON DELETE RESTRICT,
  purpose TEXT NOT NULL DEFAULT 'input' CHECK (purpose IN ('input', 'evidence', 'result', 'debug')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (operation_id, frame_ref_id)
);

CREATE INDEX IF NOT EXISTS idx_operation_frame_refs_operation_id ON operation_frame_refs (operation_id);
CREATE INDEX IF NOT EXISTS idx_operation_frame_refs_frame_ref_id ON operation_frame_refs (frame_ref_id);
CREATE INDEX IF NOT EXISTS idx_operation_frame_refs_purpose ON operation_frame_refs (purpose);

CREATE TABLE IF NOT EXISTS operator_queue_items (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  operation_result_id TEXT NOT NULL REFERENCES operation_results(id) ON DELETE CASCADE,
  operation_id TEXT NOT NULL REFERENCES operations(id) ON DELETE CASCADE,
  camera_id TEXT NOT NULL,
  camera_group_id TEXT REFERENCES camera_groups(id) ON DELETE SET NULL,
  prompt_id TEXT REFERENCES saved_prompts(id) ON DELETE SET NULL,
  frame_ref_id TEXT NOT NULL REFERENCES camera_frame_refs(id) ON DELETE RESTRICT,
  frame_url TEXT NOT NULL,
  recommended_action TEXT NOT NULL,
  reason TEXT NOT NULL,
  prompt_match_score NUMERIC(5, 2) NOT NULL DEFAULT 0 CHECK (prompt_match_score >= 0 AND prompt_match_score <= 100),
  operator_priority_score NUMERIC(5, 2) NOT NULL DEFAULT 0 CHECK (operator_priority_score >= 0 AND operator_priority_score <= 100),
  status TEXT NOT NULL DEFAULT 'queued' CHECK (status IN ('queued', 'acknowledged', 'dismissed', 'completed')),
  operator_note TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (operation_result_id)
);

CREATE INDEX IF NOT EXISTS idx_operator_queue_status ON operator_queue_items (status);
CREATE INDEX IF NOT EXISTS idx_operator_queue_camera_id ON operator_queue_items (camera_id);
CREATE INDEX IF NOT EXISTS idx_operator_queue_camera_group_id ON operator_queue_items (camera_group_id);
CREATE INDEX IF NOT EXISTS idx_operator_queue_prompt_id ON operator_queue_items (prompt_id);
CREATE INDEX IF NOT EXISTS idx_operator_queue_operator_priority ON operator_queue_items (operator_priority_score DESC);
CREATE INDEX IF NOT EXISTS idx_operator_queue_created_at ON operator_queue_items (created_at DESC);

CREATE TABLE IF NOT EXISTS gemini_caller_settings (
  id BOOLEAN PRIMARY KEY DEFAULT true CHECK (id = true),
  enabled BOOLEAN NOT NULL DEFAULT true,
  model_name TEXT NOT NULL DEFAULT 'gemini-1.5-flash',
  continuous_scan_enabled BOOLEAN NOT NULL DEFAULT false,
  continuous_scan_interval_seconds INTEGER NOT NULL DEFAULT 900 CHECK (continuous_scan_interval_seconds >= 30),
  last_continuous_scan_at TIMESTAMPTZ,
  next_continuous_scan_at TIMESTAMPTZ,
  gemini_call_delay_ms INTEGER NOT NULL DEFAULT 2000 CHECK (gemini_call_delay_ms >= 0),
  max_concurrent_gemini_calls INTEGER NOT NULL DEFAULT 1 CHECK (max_concurrent_gemini_calls >= 1),
  max_tokens_per_request INTEGER NOT NULL DEFAULT 8192,
  max_cost_per_day NUMERIC(12, 6) NOT NULL DEFAULT 10.000000,
  max_cost_per_month NUMERIC(12, 6) NOT NULL DEFAULT 100.000000,
  allow_emergency_override BOOLEAN NOT NULL DEFAULT false,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO gemini_caller_settings (id) VALUES (true) ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS usage_limit_settings (
  id BOOLEAN PRIMARY KEY DEFAULT true CHECK (id = true),
  max_scans_per_day INTEGER NOT NULL DEFAULT 1000,
  max_scans_per_month INTEGER NOT NULL DEFAULT 30000,
  max_estimated_cost_per_day NUMERIC(12, 6) NOT NULL DEFAULT 10.000000,
  max_estimated_cost_per_month NUMERIC(12, 6) NOT NULL DEFAULT 100.000000,
  block_operations_when_limit_reached BOOLEAN NOT NULL DEFAULT true,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO usage_limit_settings (id) VALUES (true) ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS usage_events (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  operation_id TEXT REFERENCES operations(id) ON DELETE SET NULL,
  camera_id TEXT,
  camera_group_id TEXT REFERENCES camera_groups(id) ON DELETE SET NULL,
  event_type TEXT NOT NULL CHECK (event_type IN ('scan', 'gemini-request', 'snapshot-fetch', 'operation')),
  estimated_cost NUMERIC(12, 6) NOT NULL DEFAULT 0,
  token_count INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_usage_events_created_at ON usage_events (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_usage_events_camera_id ON usage_events (camera_id);
CREATE INDEX IF NOT EXISTS idx_usage_events_camera_group_id ON usage_events (camera_group_id);
CREATE INDEX IF NOT EXISTS idx_usage_events_operation_id ON usage_events (operation_id);

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_camera_groups_updated_at ON camera_groups;
CREATE TRIGGER trg_camera_groups_updated_at BEFORE UPDATE ON camera_groups FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_saved_prompts_updated_at ON saved_prompts;
CREATE TRIGGER trg_saved_prompts_updated_at BEFORE UPDATE ON saved_prompts FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_prompt_bindings_updated_at ON prompt_bindings;
CREATE TRIGGER trg_prompt_bindings_updated_at BEFORE UPDATE ON prompt_bindings FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_operator_queue_items_updated_at ON operator_queue_items;
CREATE TRIGGER trg_operator_queue_items_updated_at BEFORE UPDATE ON operator_queue_items FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_camera_frame_refs_updated_at ON camera_frame_refs;
CREATE TRIGGER trg_camera_frame_refs_updated_at BEFORE UPDATE ON camera_frame_refs FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_gemini_caller_settings_updated_at ON gemini_caller_settings;
CREATE TRIGGER trg_gemini_caller_settings_updated_at BEFORE UPDATE ON gemini_caller_settings FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_usage_limit_settings_updated_at ON usage_limit_settings;
CREATE TRIGGER trg_usage_limit_settings_updated_at BEFORE UPDATE ON usage_limit_settings FOR EACH ROW EXECUTE FUNCTION set_updated_at();
