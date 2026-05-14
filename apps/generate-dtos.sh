#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

CONTAINER_RUNTIME="${CONTAINER_RUNTIME:-podman}"
GENERATOR_IMAGE="${GENERATOR_IMAGE:-docker.io/openapitools/openapi-generator-cli:v7.12.0}"

TMP_ROOT="$PROJECT_ROOT/apps/tmp/generated-dtos"

show_usage() {
  cat <<EOF_USAGE
Usage:
  ./apps/generate-dtos.sh

Behavior:
  1. Deletes and recreates apps/tmp/generated-dtos
  2. Generates OpenAPI client/DTO packages once into tmp
  3. Copies generated packages into each app's backend folder

Generated temp output:
  apps/tmp/generated-dtos/python/cambot
  apps/tmp/generated-dtos/python/camera_system_integrator
  apps/tmp/generated-dtos/javascript/CambotApi
  apps/tmp/generated-dtos/javascript/CameraSystemIntegrator

Copied Python output:
  apps/server/RestApi/backend/cambot
  apps/server/RestApi/backend/camera_system_integrator

  apps/server/GeminiCaller/backend/cambot
  apps/server/GeminiCaller/backend/camera_system_integrator

  apps/server/CameraSystemMockerRestApi/backend/cambot
  apps/server/CameraSystemMockerRestApi/backend/camera_system_integrator

Copied JavaScript output:
  apps/client/backend/CambotApi
  apps/client/backend/CameraSystemIntegrator

Environment:
  CONTAINER_RUNTIME           podman by default
  GENERATOR_IMAGE             docker.io/openapitools/openapi-generator-cli:v7.12.0 by default
  CAMBOT_SPEC_PATH            optional host path override for cambot-api.yaml
  CAMERA_SYSTEM_SPEC_PATH     optional host path override for camera-system-integrator-api.yaml
EOF_USAGE
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  show_usage
  exit 0
fi

if [[ $# -gt 0 ]]; then
  echo "Unknown argument(s): $*"
  echo
  show_usage
  exit 1
fi

require_inside_project() {
  local host_path="$1"
  local abs_path

  if [[ ! -e "$host_path" ]]; then
    echo "Missing path: $host_path" >&2
    exit 1
  fi

  abs_path="$(cd "$(dirname "$host_path")" && pwd)/$(basename "$host_path")"

  case "$abs_path" in
    "$PROJECT_ROOT"/*|"$PROJECT_ROOT")
      echo "$abs_path"
      ;;
    *)
      echo "Path must be inside the project root." >&2
      echo "Project root: $PROJECT_ROOT" >&2
      echo "Path:         $abs_path" >&2
      exit 1
      ;;
  esac
}

to_container_file_path() {
  local host_file="$1"
  local abs_file
  abs_file="$(require_inside_project "$host_file")"
  echo "/workspace${abs_file#"$PROJECT_ROOT"}"
}

to_container_dir_path() {
  local host_dir="$1"
  local abs_dir

  mkdir -p "$host_dir"
  abs_dir="$(cd "$host_dir" && pwd)"

  case "$abs_dir" in
    "$PROJECT_ROOT"/*)
      echo "/workspace${abs_dir#"$PROJECT_ROOT"}"
      ;;
    "$PROJECT_ROOT")
      echo "/workspace"
      ;;
    *)
      echo "Path must be inside the project root." >&2
      echo "Project root: $PROJECT_ROOT" >&2
      echo "Path:         $abs_dir" >&2
      exit 1
      ;;
  esac
}

find_spec() {
  local env_var_name="$1"
  local expected_name="$2"
  shift 2

  local candidates=("$@")
  local override="${!env_var_name:-}"

  if [[ -n "$override" ]]; then
    require_inside_project "$override" >/dev/null
    echo "$override"
    return 0
  fi

  for candidate in "${candidates[@]}"; do
    if [[ -f "$candidate" ]]; then
      echo "$candidate"
      return 0
    fi
  done

  local found
  found="$(
    find "$PROJECT_ROOT/apps/contracts" \
      -type f \
      \( -name "$expected_name" -o -name "${expected_name%.yaml}.yml" \) \
      2>/dev/null | head -n 1 || true
  )"

  if [[ -n "$found" ]]; then
    echo "$found"
    return 0
  fi

  echo "Could not find OpenAPI spec: $expected_name" >&2
  echo "Files under apps/contracts:" >&2
  find "$PROJECT_ROOT/apps/contracts" -maxdepth 4 -type f 2>/dev/null | sort >&2 || true
  exit 1
}

run_generator() {
  "$CONTAINER_RUNTIME" run --rm \
    -v "$PROJECT_ROOT:/workspace:Z" \
    "$GENERATOR_IMAGE" "$@"
}

reset_dir() {
  local dir="$1"
  rm -rf "$dir"
  mkdir -p "$dir"
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

  # Copy contents, not the containing folder.
  cp -a "$src/." "$dst/"
}

generate_python() {
  local spec_host="$1"
  local host_output="$2"
  local package_name="$3"
  local project_name="$4"

  local spec_container
  local container_output

  reset_dir "$host_output"

  spec_container="$(to_container_file_path "$spec_host")"
  container_output="$(to_container_dir_path "$host_output")"

  run_generator generate -i "$spec_container" -g python \
    -o "$container_output" \
    --additional-properties=packageName="$package_name",projectName="$project_name"
}

generate_javascript() {
  local spec_host="$1"
  local host_output="$2"
  local project_name="$3"

  local spec_container
  local container_output

  reset_dir "$host_output"

  spec_container="$(to_container_file_path "$spec_host")"
  container_output="$(to_container_dir_path "$host_output")"

  run_generator generate -i "$spec_container" -g javascript \
    -o "$container_output" \
    --additional-properties=projectName="$project_name",usePromises=true,useES6=true
}

CAMBOT_SPEC_HOST="$(
  find_spec \
    CAMBOT_SPEC_PATH \
    cambot-api.yaml \
    "$PROJECT_ROOT/apps/contracts/cambot-api.yaml" \
    "$PROJECT_ROOT/apps/contracts/cambot-api.yml" \
    "$PROJECT_ROOT/apps/contracts/openapi/cambot-api.yaml" \
    "$PROJECT_ROOT/apps/contracts/openapi/cambot-api.yml"
)"

CAMERA_SYSTEM_SPEC_HOST="$(
  find_spec \
    CAMERA_SYSTEM_SPEC_PATH \
    camera-system-integrator-api.yaml \
    "$PROJECT_ROOT/apps/contracts/camera-system-integrator-api.yaml" \
    "$PROJECT_ROOT/apps/contracts/camera-system-integrator-api.yml" \
    "$PROJECT_ROOT/apps/contracts/openapi/camera-system-integrator-api.yaml" \
    "$PROJECT_ROOT/apps/contracts/openapi/camera-system-integrator-api.yml"
)"

CAMBOT_SPEC_CONTAINER="$(to_container_file_path "$CAMBOT_SPEC_HOST")"
CAMERA_SYSTEM_SPEC_CONTAINER="$(to_container_file_path "$CAMERA_SYSTEM_SPEC_HOST")"

TMP_PY_CAMBOT="$TMP_ROOT/python/cambot"
TMP_PY_CAMERA_SYSTEM="$TMP_ROOT/python/camera_system_integrator"
TMP_JS_CAMBOT="$TMP_ROOT/javascript/CambotApi"
TMP_JS_CAMERA_SYSTEM="$TMP_ROOT/javascript/CameraSystemIntegrator"

PYTHON_SERVICES=(
  "RestApi"
  "GeminiCaller"
  "CameraSystemMockerRestApi"
)

echo "Project root:"
echo "  $PROJECT_ROOT"
echo

echo "OpenAPI specs:"
echo "  CamBot API:                 $CAMBOT_SPEC_HOST"
echo "  Camera System Integrator:   $CAMERA_SYSTEM_SPEC_HOST"
echo

echo "Resetting temp generated DTO folder:"
echo "  $TMP_ROOT"
rm -rf "$TMP_ROOT"
mkdir -p "$TMP_ROOT"

echo
echo "Validating OpenAPI specs..."
run_generator validate -i "$CAMBOT_SPEC_CONTAINER"
run_generator validate -i "$CAMERA_SYSTEM_SPEC_CONTAINER"

echo
echo "Generating CamBot Python DTO/client package into tmp..."
generate_python "$CAMBOT_SPEC_HOST" "$TMP_PY_CAMBOT" \
  "cambot_dtos" "cambot-dtos"

echo
echo "Generating Camera System Python DTO/client package into tmp..."
generate_python "$CAMERA_SYSTEM_SPEC_HOST" "$TMP_PY_CAMERA_SYSTEM" \
  "camera_system_integrator_dtos" "camera-system-integrator-dtos"

echo
echo "Generating CamBot JavaScript DTO/client package into tmp..."
generate_javascript "$CAMBOT_SPEC_HOST" "$TMP_JS_CAMBOT" \
  "cambot-api"

echo
echo "Generating Camera System JavaScript DTO/client package into tmp..."
generate_javascript "$CAMERA_SYSTEM_SPEC_HOST" "$TMP_JS_CAMERA_SYSTEM" \
  "camera-system-integrator-api"

echo
echo "Copying generated Python packages into server apps..."

for service in "${PYTHON_SERVICES[@]}"; do
  echo "  $service"

  copy_generated_dir "$TMP_PY_CAMBOT" \
    "$PROJECT_ROOT/apps/server/$service/backend/cambot"

  copy_generated_dir "$TMP_PY_CAMERA_SYSTEM" \
    "$PROJECT_ROOT/apps/server/$service/backend/camera_system_integrator"
done

echo
echo "Copying generated JavaScript packages into client app..."

copy_generated_dir "$TMP_JS_CAMBOT" \
  "$PROJECT_ROOT/apps/client/backend/CambotApi"

copy_generated_dir "$TMP_JS_CAMERA_SYSTEM" \
  "$PROJECT_ROOT/apps/client/backend/CameraSystemIntegrator"

echo
echo "DTO/client generation complete."
echo
echo "Generated temp output:"
echo "  $TMP_ROOT"
echo
echo "Copied project output:"
for service in "${PYTHON_SERVICES[@]}"; do
  echo "  apps/server/$service/backend/cambot"
  echo "  apps/server/$service/backend/camera_system_integrator"
done
echo
echo "  apps/client/backend/CambotApi"
echo "  apps/client/backend/CameraSystemIntegrator"
