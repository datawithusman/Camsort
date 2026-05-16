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
  prompt_type TEXT NOT NULL CHECK (prompt_type IN ('sorting', 'finding', 'monitoring', 'summarization')),
  description TEXT,
  prompt_text TEXT NOT NULL,
  default_priority TEXT NOT NULL DEFAULT 'normal' CHECK (default_priority IN ('low', 'normal', 'high', 'emergency')),
  default_max_estimated_cost NUMERIC(12, 6),
  enabled BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_saved_prompts_prompt_type ON saved_prompts (prompt_type);
CREATE INDEX IF NOT EXISTS idx_saved_prompts_enabled ON saved_prompts (enabled);

CREATE TABLE IF NOT EXISTS prompt_bindings (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  camera_group_id TEXT NOT NULL REFERENCES camera_groups(id) ON DELETE CASCADE,
  prompt_id TEXT NOT NULL REFERENCES saved_prompts(id) ON DELETE CASCADE,
  enabled BOOLEAN NOT NULL DEFAULT true,
  scan_frequency TEXT NOT NULL DEFAULT 'manual' CHECK (scan_frequency IN ('manual', 'hourly', 'daily', 'continuous')),
  priority_override TEXT CHECK (priority_override IS NULL OR priority_override IN ('low', 'normal', 'high', 'emergency')),
  max_estimated_cost_override NUMERIC(12, 6),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (camera_group_id, prompt_id)
);

CREATE INDEX IF NOT EXISTS idx_prompt_bindings_camera_group_id ON prompt_bindings (camera_group_id);
CREATE INDEX IF NOT EXISTS idx_prompt_bindings_prompt_id ON prompt_bindings (prompt_id);
CREATE INDEX IF NOT EXISTS idx_prompt_bindings_enabled ON prompt_bindings (enabled);

CREATE TABLE IF NOT EXISTS operations (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
  operation_type TEXT NOT NULL CHECK (operation_type IN ('find', 'sort', 'scan', 'summarize', 'monitor')),
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
  target_type TEXT NOT NULL CHECK (target_type IN ('camera', 'camera-group', 'facility')),
  target_camera_id TEXT,
  target_camera_group_id TEXT REFERENCES camera_groups(id) ON DELETE SET NULL,
  saved_prompt_id TEXT REFERENCES saved_prompts(id) ON DELETE SET NULL,
  temporary_prompt_text TEXT,
  allowed BOOLEAN,
  restriction_reason TEXT,
  estimated_camera_count INTEGER NOT NULL DEFAULT 0,
  estimated_prompt_count INTEGER NOT NULL DEFAULT 0,
  estimated_token_count INTEGER NOT NULL DEFAULT 0,
  estimated_cost NUMERIC(12, 6) NOT NULL DEFAULT 0,
  max_estimated_cost NUMERIC(12, 6),
  error_message TEXT,
  result_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  CHECK (
    (target_type = 'camera' AND target_camera_id IS NOT NULL)
    OR (target_type = 'camera-group' AND target_camera_group_id IS NOT NULL)
    OR (target_type = 'facility')
  )
);

CREATE INDEX IF NOT EXISTS idx_operations_status ON operations (status);
CREATE INDEX IF NOT EXISTS idx_operations_operation_type ON operations (operation_type);
CREATE INDEX IF NOT EXISTS idx_operations_target_camera_id ON operations (target_camera_id);
CREATE INDEX IF NOT EXISTS idx_operations_target_camera_group_id ON operations (target_camera_group_id);
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
  operation_id TEXT REFERENCES operations(id) ON DELETE SET NULL,
  camera_id TEXT NOT NULL,
  camera_group_id TEXT REFERENCES camera_groups(id) ON DELETE SET NULL,
  saved_prompt_id TEXT REFERENCES saved_prompts(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  recommended_action TEXT,
  confidence NUMERIC(5, 4) NOT NULL DEFAULT 0 CHECK (confidence >= 0 AND confidence <= 1),
  urgency NUMERIC(5, 4) NOT NULL DEFAULT 0 CHECK (urgency >= 0 AND urgency <= 1),
  risk NUMERIC(5, 4) NOT NULL DEFAULT 0 CHECK (risk >= 0 AND risk <= 1),
  overall NUMERIC(5, 4) NOT NULL DEFAULT 0 CHECK (overall >= 0 AND overall <= 1),
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'acknowledged', 'dismissed', 'completed')),
  operator_note TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_operator_queue_status ON operator_queue_items (status);
CREATE INDEX IF NOT EXISTS idx_operator_queue_camera_id ON operator_queue_items (camera_id);
CREATE INDEX IF NOT EXISTS idx_operator_queue_camera_group_id ON operator_queue_items (camera_group_id);
CREATE INDEX IF NOT EXISTS idx_operator_queue_overall ON operator_queue_items (overall DESC);
CREATE INDEX IF NOT EXISTS idx_operator_queue_created_at ON operator_queue_items (created_at DESC);

CREATE TABLE IF NOT EXISTS gemini_caller_settings (
  id BOOLEAN PRIMARY KEY DEFAULT true CHECK (id = true),
  enabled BOOLEAN NOT NULL DEFAULT true,
  model_name TEXT NOT NULL DEFAULT 'gemini-1.5-flash',
  max_requests_per_minute INTEGER NOT NULL DEFAULT 30,
  max_tokens_per_request INTEGER NOT NULL DEFAULT 8192,
  max_cost_per_operation NUMERIC(12, 6) NOT NULL DEFAULT 1.000000,
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
