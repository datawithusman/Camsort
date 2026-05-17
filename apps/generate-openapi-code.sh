#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

CONTAINER_RUNTIME="${CONTAINER_RUNTIME:-podman}"
OPENAPI_GENERATOR_IMAGE="${OPENAPI_GENERATOR_IMAGE:-docker.io/openapitools/openapi-generator-cli:v7.12.0}"

CONTRACTS_DIR="$PROJECT_ROOT/apps/contracts"
OPENAPI_CONTRACTS_DIR="$CONTRACTS_DIR/openapi"

TMP_DTO_ROOT="$PROJECT_ROOT/apps/tmp/generated-dtos"

TMP_PY_CAMBOT="$TMP_DTO_ROOT/python/cambot"
TMP_PY_CAMERA_SYSTEM="$TMP_DTO_ROOT/python/camera_system_integrator"

TMP_JS_CAMBOT="$TMP_DTO_ROOT/javascript/CambotApi"
TMP_JS_CAMERA_SYSTEM="$TMP_DTO_ROOT/javascript/CameraSystemIntegrator"

PYTHON_SERVICES=(
  "RestApi"
  "GeminiCaller"
  "CameraSystemMockerRestApi"
)

show_usage() {
  cat <<EOF_USAGE
Usage:
  ./apps/generate-open-api.sh

Generates OpenAPI-derived code from:

  apps/contracts/openapi/cambot-api.yaml
  apps/contracts/openapi/camera-system-integrator-api.yaml

Generated temp output:

  apps/tmp/generated-dtos/python/cambot
  apps/tmp/generated-dtos/python/camera_system_integrator
  apps/tmp/generated-dtos/javascript/CambotApi
  apps/tmp/generated-dtos/javascript/CameraSystemIntegrator

Copied Python service output:

  apps/server/<Service>/backend/cambot
  apps/server/<Service>/backend/camera_system_integrator

Copied frontend output:

  apps/client/backend/CambotApi
  apps/client/backend/CameraSystemIntegrator

Environment:
  CONTAINER_RUNTIME             podman by default
  OPENAPI_GENERATOR_IMAGE       docker.io/openapitools/openapi-generator-cli:v7.12.0 by default
  CAMBOT_SPEC_PATH              optional override for cambot-api.yaml
  CAMERA_SYSTEM_SPEC_PATH       optional override for camera-system-integrator-api.yaml
EOF_USAGE
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  show_usage
  exit 0
fi

if [[ $# -gt 0 ]]; then
  echo "Unknown argument(s): $*" >&2
  echo >&2
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
    find "$CONTRACTS_DIR" \
      -type f \
      \( -name "$expected_name" -o -name "${expected_name%.yaml}.yml" \) \
      2>/dev/null | head -n 1 || true
  )"

  if [[ -n "$found" ]]; then
    echo "$found"
    return 0
  fi

  echo "Could not find OpenAPI spec: $expected_name" >&2
  echo "Expected OpenAPI directory:" >&2
  echo "  $OPENAPI_CONTRACTS_DIR" >&2
  echo >&2
  echo "Files under apps/contracts:" >&2
  find "$CONTRACTS_DIR" -maxdepth 6 -type f 2>/dev/null | sort >&2 || true
  exit 1
}

run_openapi_generator() {
  "$CONTAINER_RUNTIME" run --rm \
    -v "$PROJECT_ROOT:/workspace:Z" \
    "$OPENAPI_GENERATOR_IMAGE" "$@"
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
  cp -a "$src/." "$dst/"
}

generate_python_openapi() {
  local spec_host="$1"
  local host_output="$2"
  local package_name="$3"
  local project_name="$4"

  local spec_container
  local container_output

  reset_dir "$host_output"

  spec_container="$(to_container_file_path "$spec_host")"
  container_output="$(to_container_dir_path "$host_output")"

  echo
  echo "Generating Python package:"
  echo "  spec:    $spec_host"
  echo "  output:  $host_output"
  echo "  package: $package_name"

  run_openapi_generator generate -i "$spec_container" -g python \
    -o "$container_output" \
    --additional-properties=packageName="$package_name",projectName="$project_name"
}

generate_javascript_openapi() {
  local spec_host="$1"
  local host_output="$2"
  local project_name="$3"

  local spec_container
  local container_output

  reset_dir "$host_output"

  spec_container="$(to_container_file_path "$spec_host")"
  container_output="$(to_container_dir_path "$host_output")"

  echo
  echo "Generating JavaScript package:"
  echo "  spec:    $spec_host"
  echo "  output:  $host_output"

  run_openapi_generator generate -i "$spec_container" -g javascript \
    -o "$container_output" \
    --additional-properties=projectName="$project_name",usePromises=true,useES6=true
}

echo "Project root:"
echo "  $PROJECT_ROOT"
echo

CAMBOT_SPEC_HOST="$(
  find_spec \
    CAMBOT_SPEC_PATH \
    cambot-api.yaml \
    "$OPENAPI_CONTRACTS_DIR/cambot-api.yaml" \
    "$OPENAPI_CONTRACTS_DIR/cambot-api.yml"
)"

CAMERA_SYSTEM_SPEC_HOST="$(
  find_spec \
    CAMERA_SYSTEM_SPEC_PATH \
    camera-system-integrator-api.yaml \
    "$OPENAPI_CONTRACTS_DIR/camera-system-integrator-api.yaml" \
    "$OPENAPI_CONTRACTS_DIR/camera-system-integrator-api.yml"
)"

CAMBOT_SPEC_CONTAINER="$(to_container_file_path "$CAMBOT_SPEC_HOST")"
CAMERA_SYSTEM_SPEC_CONTAINER="$(to_container_file_path "$CAMERA_SYSTEM_SPEC_HOST")"

echo "=== OpenAPI contract generation ==="
echo
echo "CamBot API:"
echo "  $CAMBOT_SPEC_HOST"
echo "Camera System Integrator API:"
echo "  $CAMERA_SYSTEM_SPEC_HOST"
echo
echo "Resetting OpenAPI temp output:"
echo "  $TMP_DTO_ROOT"

rm -rf "$TMP_DTO_ROOT"
mkdir -p "$TMP_DTO_ROOT"

echo
echo "Validating OpenAPI specs..."
run_openapi_generator validate -i "$CAMBOT_SPEC_CONTAINER"
run_openapi_generator validate -i "$CAMERA_SYSTEM_SPEC_CONTAINER"

echo
echo "Generating Python OpenAPI packages..."

generate_python_openapi "$CAMBOT_SPEC_HOST" "$TMP_PY_CAMBOT" \
  "cambot_dtos" "cambot-dtos"

generate_python_openapi "$CAMERA_SYSTEM_SPEC_HOST" "$TMP_PY_CAMERA_SYSTEM" \
  "camera_system_integrator_dtos" "camera-system-integrator-dtos"

echo
echo "Generating JavaScript OpenAPI packages..."

generate_javascript_openapi "$CAMBOT_SPEC_HOST" "$TMP_JS_CAMBOT" \
  "cambot-api"

generate_javascript_openapi "$CAMERA_SYSTEM_SPEC_HOST" "$TMP_JS_CAMERA_SYSTEM" \
  "camera-system-integrator-api"

echo
echo "Copying OpenAPI Python packages into Python services..."

for service in "${PYTHON_SERVICES[@]}"; do
  echo "  $service"

  copy_generated_dir "$TMP_PY_CAMBOT" \
    "$PROJECT_ROOT/apps/server/$service/backend/cambot"

  copy_generated_dir "$TMP_PY_CAMERA_SYSTEM" \
    "$PROJECT_ROOT/apps/server/$service/backend/camera_system_integrator"
done

echo
echo "Copying OpenAPI JavaScript packages into client..."

copy_generated_dir "$TMP_JS_CAMBOT" \
  "$PROJECT_ROOT/apps/client/backend/CambotApi"

copy_generated_dir "$TMP_JS_CAMERA_SYSTEM" \
  "$PROJECT_ROOT/apps/client/backend/CameraSystemIntegrator"

echo
echo "=== OpenAPI contract code generation complete ==="
echo
echo "Generated temp output:"
echo "  $TMP_DTO_ROOT"
echo
echo "Copied Python service output:"
for service in "${PYTHON_SERVICES[@]}"; do
  echo "  apps/server/$service/backend/cambot"
  echo "  apps/server/$service/backend/camera_system_integrator"
done
echo
echo "Copied frontend output:"
echo "  apps/client/backend/CambotApi"
echo "  apps/client/backend/CameraSystemIntegrator"
