#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

CONTAINER_RUNTIME="${CONTAINER_RUNTIME:-podman}"
SQLC_IMAGE="${SQLC_IMAGE:-docker.io/sqlc/sqlc:latest}"

POSTGRES_CONTRACTS_DIR="$PROJECT_ROOT/apps/contracts/postgres"
TMP_SQL_ROOT="$PROJECT_ROOT/apps/tmp/generated-sql"
TMP_DB_OUT="$TMP_SQL_ROOT/python/db"

PYTHON_SERVICES=(
  "RestApi"
  "GeminiCaller"
  "CameraSystemMockerRestApi"
)

run_sqlc() {
  "$CONTAINER_RUNTIME" run --rm \
    -v "$PROJECT_ROOT:/src:Z" \
    -w /src \
    "$SQLC_IMAGE" "$@"
}

copy_generated_dir() {
  local src="$1"
  local dst="$2"

  if [[ ! -d "$src" ]]; then
    echo "Missing generated source directory: $src" >&2
    exit 1
  fi

  rm -rf "$dst"
  mkdir -p "$dst"
  cp -a "$src/." "$dst/"
}

echo "Project root:"
echo "  $PROJECT_ROOT"
echo

echo "=== Postgres contract generation ==="
echo

sqlc_config="$POSTGRES_CONTRACTS_DIR/sqlc.yaml"

if [[ ! -f "$sqlc_config" ]]; then
  echo "Missing sqlc config:" >&2
  echo "  $sqlc_config" >&2
  exit 1
fi

if [[ ! -d "$POSTGRES_CONTRACTS_DIR/schema" ]]; then
  echo "Missing Postgres schema directory:" >&2
  echo "  $POSTGRES_CONTRACTS_DIR/schema" >&2
  exit 1
fi

if [[ ! -d "$POSTGRES_CONTRACTS_DIR/queries" ]]; then
  echo "Missing Postgres queries directory:" >&2
  echo "  $POSTGRES_CONTRACTS_DIR/queries" >&2
  exit 1
fi

echo "Resetting SQL temp output:"
echo "  $TMP_SQL_ROOT"
rm -rf "$TMP_SQL_ROOT"
mkdir -p "$TMP_DB_OUT"

echo
echo "Running sqlc..."
echo "  $CONTAINER_RUNTIME run --rm -v \"$PROJECT_ROOT:/src:Z\" -w /src \"$SQLC_IMAGE\" generate -f apps/contracts/postgres/sqlc.yaml"
echo

run_sqlc generate -f apps/contracts/postgres/sqlc.yaml

echo
echo "Checking generated output:"
echo "  $TMP_DB_OUT"

if [[ ! -d "$TMP_DB_OUT" ]]; then
  echo "sqlc completed, but expected output directory is missing:" >&2
  echo "  $TMP_DB_OUT" >&2
  echo
  echo "Check apps/contracts/postgres/sqlc.yaml. Its output should be:" >&2
  echo "  apps/tmp/generated-sql/python/db" >&2
  exit 1
fi

echo
echo "Generated files:"
find "$TMP_DB_OUT" -maxdepth 2 -type f | sort

echo
echo "Checking for new contract fields..."
grep -R "prompt_match_score\|operator_priority_score\|operation_result_id\|interval_seconds" -n "$TMP_DB_OUT" || {
  echo "Warning: expected new fields were not found in generated DB code." >&2
}

echo
echo "Checking for old contract fields..."
if grep -R "prompt_type\|operation_type\|scan_frequency\|confidence\|urgency\|risk\|overall" -n "$TMP_DB_OUT"; then
  echo "Warning: old fields still exist in generated DB code." >&2
fi

echo
echo "Copying generated DB package into Python services..."

for service in "${PYTHON_SERVICES[@]}"; do
  echo "  $service"
  copy_generated_dir "$TMP_DB_OUT" \
    "$PROJECT_ROOT/apps/server/$service/backend/db"
done

echo
echo "=== DB contract code generation complete ==="
