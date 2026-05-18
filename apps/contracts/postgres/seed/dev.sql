INSERT INTO camera_groups (id, name, description, camera_ids)
VALUES
  (
    'group-all',
    'All Cameras',
    'Default operational group for all demo cameras.',
    ARRAY[
      'cam01','cam02','cam03','cam04','cam05','cam06','cam07','cam08','cam09','cam10',
      'cam11','cam12','cam13','cam14','cam15','cam16','cam17','cam18','cam19','cam20',
      'cam21','cam22','cam23','cam24','cam25','cam26','cam27','cam28','cam29','cam30',
      'cam31','cam32','cam33','cam34','cam35','cam36','cam37','cam38','cam39','cam40',
      'cam41','cam42','cam43','cam44','cam45','cam46','cam47','cam48','cam49','cam50'
    ]::text[]
  ),
  (
    'group-entrances',
    'Entrances',
    'Demo group for entrance-focused prompt scans.',
    ARRAY[
      'cam01','cam02','cam03','cam04','cam05',
      'cam06','cam07','cam08','cam09','cam10'
    ]::text[]
  ),
  (
    'group-parking',
    'Parking',
    'Demo group for parking-area prompt scans.',
    ARRAY[
      'cam11','cam12','cam13','cam14','cam15',
      'cam16','cam17','cam18','cam19','cam20'
    ]::text[]
  ),
  (
    'group-south-building',
    'South Building',
    'Demo group for south-building prompt scans.',
    ARRAY[
      'cam21','cam22','cam23','cam24','cam25',
      'cam26','cam27','cam28','cam29','cam30'
    ]::text[]
  )
ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  camera_ids = EXCLUDED.camera_ids,
  updated_at = now();

INSERT INTO saved_prompts (id, name, description, prompt_text, enabled)
VALUES
  (
    'prompt-after-hours-activity',
    'Find after-hours activity',
    'Find people or activity near restricted areas after hours.',
    'Inspect this camera snapshot for people, vehicles, or suspicious movement near restricted entrances after hours. Return first-pass JSON with include, firstPassPromptScore from 0 to 100, operatorPriorityScore from 0 to 100, operatorAction, and reason.',
    true
  ),
  (
    'prompt-ice-near-entrances',
    'Ice near entrances',
    'Find icy, slick, snowy, or blocked entrance conditions that may require staff action.',
    'Inspect this camera snapshot for ice, snow, slick surfaces, blocked entrance paths, or other entrance safety issues. Return first-pass JSON with include, firstPassPromptScore from 0 to 100, operatorPriorityScore from 0 to 100, operatorAction, and reason.',
    true
  )
ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  prompt_text = EXCLUDED.prompt_text,
  enabled = EXCLUDED.enabled,
  updated_at = now();

INSERT INTO prompt_bindings (id, camera_group_id, prompt_id, enabled)
VALUES
  (
    'binding-entrances-ice',
    'group-entrances',
    'prompt-ice-near-entrances',
    true
  )
ON CONFLICT (camera_group_id, prompt_id) DO UPDATE SET
  enabled = EXCLUDED.enabled,
  updated_at = now();
