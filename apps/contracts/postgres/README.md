# CamBot Postgres Contract

This folder is the database source of truth for CamBot.

## Layout

```text
apps/postgres/
  schema/
    001_init.sql
  queries/
    camera_groups.sql
    saved_prompts.sql
    prompt_bindings.sql
    operations.sql
    operator_queue.sql
    settings.sql
    usage.sql
  seed/
    dev.sql
```

## Intended architecture

```text
apps/contracts/
  OpenAPI contracts

apps/postgres/
  SQL/Postgres contract

apps/server/<service>/backend/
  generated code copied into each Python container

apps/server/<service>/app/
  handwritten service code
```

Keep handwritten repository/wrapper code under `app/`, not under `backend/`, because generated folders may be deleted/recreated.
