-- name: CreateUsageEvent :one
INSERT INTO usage_events (id, operation_id, camera_id, camera_group_id, event_type, estimated_cost, token_count)
VALUES (COALESCE(NULLIF($1, ''), gen_random_uuid()::text), $2, $3, $4, $5, COALESCE($6, 0), COALESCE($7, 0))
RETURNING *;

-- name: GetUsageSummary :one
SELECT
  COUNT(*) FILTER (WHERE event_type = 'scan' AND created_at >= date_trunc('day', now()))::int AS scans_today,
  COUNT(*) FILTER (WHERE event_type = 'scan' AND created_at >= date_trunc('month', now()))::int AS scans_this_month,
  COALESCE(SUM(estimated_cost) FILTER (WHERE created_at >= date_trunc('day', now())), 0)::numeric AS estimated_cost_today,
  COALESCE(SUM(estimated_cost) FILTER (WHERE created_at >= date_trunc('month', now())), 0)::numeric AS estimated_cost_this_month,
  now() AS last_updated_at
FROM usage_events;

-- name: GetUsageSummaryForCamera :one
SELECT
  COUNT(*) FILTER (WHERE event_type = 'scan' AND created_at >= date_trunc('day', now()))::int AS scans_today,
  COUNT(*) FILTER (WHERE event_type = 'scan' AND created_at >= date_trunc('month', now()))::int AS scans_this_month,
  COALESCE(SUM(estimated_cost) FILTER (WHERE created_at >= date_trunc('day', now())), 0)::numeric AS estimated_cost_today,
  COALESCE(SUM(estimated_cost) FILTER (WHERE created_at >= date_trunc('month', now())), 0)::numeric AS estimated_cost_this_month,
  now() AS last_updated_at
FROM usage_events
WHERE camera_id = $1;

-- name: GetUsageSummaryForCameraGroup :one
SELECT
  COUNT(*) FILTER (WHERE event_type = 'scan' AND created_at >= date_trunc('day', now()))::int AS scans_today,
  COUNT(*) FILTER (WHERE event_type = 'scan' AND created_at >= date_trunc('month', now()))::int AS scans_this_month,
  COALESCE(SUM(estimated_cost) FILTER (WHERE created_at >= date_trunc('day', now())), 0)::numeric AS estimated_cost_today,
  COALESCE(SUM(estimated_cost) FILTER (WHERE created_at >= date_trunc('month', now())), 0)::numeric AS estimated_cost_this_month,
  now() AS last_updated_at
FROM usage_events
WHERE camera_group_id = $1;
