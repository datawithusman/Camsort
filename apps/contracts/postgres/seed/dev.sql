INSERT INTO camera_groups (id, name, description, camera_ids)
VALUES
  (
    'group-all',
    'All Cameras',
    'Default operational group for all demo cameras.',
    ARRAY['cam01','cam02','cam03','cam04','cam05','cam06','cam07','cam08','cam09','cam10']::text[]
  ),
  (
    'group-entrances',
    'Entrances',
    'Demo group for entrance-focused prompt scans.',
    ARRAY['cam01','cam02','cam03']::text[]
  )
ON CONFLICT (id) DO NOTHING;

INSERT INTO saved_prompts (id, name, description, prompt_text, enabled)
VALUES
  (
    'prompt-after-hours-activity',
    'Find after-hours activity',
    'Find people or activity near restricted areas after hours.',
    'Inspect this camera snapshot for people, vehicles, or suspicious movement near restricted entrances after hours. Return JSON with include, promptMatchScore from 0 to 100, operatorPriorityScore from 0 to 100, recommendedAction, and reason.',
    true
  ),
  (
    'prompt-ice-near-entrances',
    'Ice near entrances',
    'Find icy, slick, snowy, or blocked entrance conditions that may require staff action.',
    'Inspect this camera snapshot for ice, snow, slick surfaces, blocked entrance paths, or other entrance safety issues. Return JSON with include, promptMatchScore from 0 to 100, operatorPriorityScore from 0 to 100, recommendedAction, and reason.',
    true
  )
ON CONFLICT (id) DO NOTHING;

INSERT INTO prompt_bindings (id, camera_group_id, prompt_id, enabled)
VALUES
  (
    'binding-entrances-ice',
    'group-entrances',
    'prompt-ice-near-entrances',
    true
  )
ON CONFLICT (camera_group_id, prompt_id) DO NOTHING;
