INSERT INTO camera_groups (id, name, description, camera_ids)
VALUES
  (
    'group-all',
    'All Cameras',
    'Default operational group for all demo cameras.',
    ARRAY['cam01','cam02','cam03','cam04','cam05','cam06','cam07','cam08','cam09','cam10']::text[]
  )
ON CONFLICT (id) DO NOTHING;

INSERT INTO saved_prompts (id, name, prompt_type, description, prompt_text, default_priority, enabled)
VALUES
  (
    'prompt-after-hours-activity',
    'Find after-hours activity',
    'finding',
    'Find people or activity near restricted areas after hours.',
    'Find people, vehicles, or suspicious movement near restricted entrances after hours.',
    'normal',
    true
  ),
  (
    'prompt-summarize-camera-group',
    'Summarize camera group',
    'summarization',
    'Summarize visible activity across a camera group.',
    'Summarize the important visual activity across these camera snapshots.',
    'normal',
    true
  )
ON CONFLICT (id) DO NOTHING;
