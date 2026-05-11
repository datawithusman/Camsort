#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

CONTAINER_RUNTIME="${CONTAINER_RUNTIME:-podman}"
GENERATOR_IMAGE="${GENERATOR_IMAGE:-docker.io/openapitools/openapi-generator-cli:v7.12.0}"

CAMBOT_SPEC="/workspace/apps/contracts/openapi/cambot-api.yaml"
CAMERA_SYSTEM_INTEGRATOR_SPEC="/workspace/apps/contracts/openapi/camera-system-integrator-api.yaml"

OUTPUT_ROOT=""

show_usage() {
  cat <<EOF
Usage:
  ./apps/generate-dtos.sh --output-dir <folder>

Examples:
  ./apps/generate-dtos.sh --output-dir ./generated/dtos
  ./apps/generate-dtos.sh --output-dir /tmp/cambot-dtos

Environment:
  CONTAINER_RUNTIME   podman by default
  GENERATOR_IMAGE     docker.io/openapitools/openapi-generator-cli:v7.12.0 by default
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-dir|-o)
      OUTPUT_ROOT="${2:-}"
      shift 2
      ;;

    --help|-h)
      show_usage
      exit 0
      ;;

    *)
      echo "Unknown argument: $1"
      echo
      show_usage
      exit 1
      ;;
  esac
done

if [[ -z "$OUTPUT_ROOT" ]]; then
  echo "Missing required argument: --output-dir"
  echo
  show_usage
  exit 1
fi

mkdir -p "$OUTPUT_ROOT"
OUTPUT_ROOT="$(cd "$OUTPUT_ROOT" && pwd)"

# Convert host output path into the corresponding container path.
# Since PROJECT_ROOT is mounted as /workspace, output must be inside PROJECT_ROOT.
case "$OUTPUT_ROOT" in
  "$PROJECT_ROOT"/*)
    CONTAINER_OUTPUT_ROOT="/workspace${OUTPUT_ROOT#"$PROJECT_ROOT"}"
    ;;
  "$PROJECT_ROOT")
    CONTAINER_OUTPUT_ROOT="/workspace"
    ;;
  *)
    echo "Output directory must be inside the project root."
    echo "Project root: $PROJECT_ROOT"
    echo "Output root:  $OUTPUT_ROOT"
    exit 1
    ;;
esac

run_generator() {
  "$CONTAINER_RUNTIME" run --rm \
    -v "$PROJECT_ROOT:/workspace" \
    "$GENERATOR_IMAGE" "$@"
}

reset_dir() {
  local dir="$1"
  rm -rf "$dir"
  mkdir -p "$dir"
}

echo "DTO/client output root:"
echo "  $OUTPUT_ROOT"
echo

echo "Validating OpenAPI specs..."
run_generator validate -i "$CAMBOT_SPEC"
run_generator validate -i "$CAMERA_SYSTEM_INTEGRATOR_SPEC"

echo "Generating Python client/DTO package for RestApi..."
reset_dir "$OUTPUT_ROOT/python/RestApi/cambot"
reset_dir "$OUTPUT_ROOT/python/RestApi/camera_system_integrator"

run_generator generate -i "$CAMBOT_SPEC" -g python \
  -o "$CONTAINER_OUTPUT_ROOT/python/RestApi/cambot" \
  --additional-properties=packageName=cambot_dtos,projectName=cambot-dtos

run_generator generate -i "$CAMERA_SYSTEM_INTEGRATOR_SPEC" -g python \
  -o "$CONTAINER_OUTPUT_ROOT/python/RestApi/camera_system_integrator" \
  --additional-properties=packageName=camera_system_integrator_dtos,projectName=camera-system-integrator-dtos

echo "Generating Python client/DTO packages for GeminiCaller..."
reset_dir "$OUTPUT_ROOT/python/GeminiCaller/cambot"
reset_dir "$OUTPUT_ROOT/python/GeminiCaller/camera_system_integrator"

run_generator generate -i "$CAMBOT_SPEC" -g python \
  -o "$CONTAINER_OUTPUT_ROOT/python/GeminiCaller/cambot" \
  --additional-properties=packageName=cambot_dtos,projectName=cambot-dtos

run_generator generate -i "$CAMERA_SYSTEM_INTEGRATOR_SPEC" -g python \
  -o "$CONTAINER_OUTPUT_ROOT/python/GeminiCaller/camera_system_integrator" \
  --additional-properties=packageName=camera_system_integrator_dtos,projectName=camera-system-integrator-dtos

echo "Generating Python client/DTO package for CameraSystemMockerRestApi..."
reset_dir "$OUTPUT_ROOT/python/CameraSystemMockerRestApi/camera_system_integrator"

run_generator generate -i "$CAMERA_SYSTEM_INTEGRATOR_SPEC" -g python \
  -o "$CONTAINER_OUTPUT_ROOT/python/CameraSystemMockerRestApi/camera_system_integrator" \
  --additional-properties=packageName=camera_system_integrator_dtos,projectName=camera-system-integrator-dtos

echo "Generating JavaScript frontend client/DTO package for CamBot API..."
reset_dir "$OUTPUT_ROOT/javascript/client/CambotApi"

run_generator generate -i "$CAMBOT_SPEC" -g javascript \
  -o "$CONTAINER_OUTPUT_ROOT/javascript/client/CambotApi" \
  --additional-properties=projectName=cambot-api,usePromises=true,useES6=true

echo "Generating JavaScript frontend client/DTO package for Camera System Integrator API..."
reset_dir "$OUTPUT_ROOT/javascript/client/CameraSystemIntegrator"

run_generator generate -i "$CAMERA_SYSTEM_INTEGRATOR_SPEC" -g javascript \
  -o "$CONTAINER_OUTPUT_ROOT/javascript/client/CameraSystemIntegrator" \
  --additional-properties=projectName=camera-system-integrator-api,usePromises=true,useES6=true

echo
echo "DTO/client generation complete."
echo
echo "Generated output:"
echo "  Python RestApi:"
echo "    $OUTPUT_ROOT/python/RestApi/cambot"
echo "    $OUTPUT_ROOT/python/RestApi/camera_system_integrator"
echo
echo "  Python GeminiCaller:"
echo "    $OUTPUT_ROOT/python/GeminiCaller/cambot"
echo "    $OUTPUT_ROOT/python/GeminiCaller/camera_system_integrator"
echo
echo "  Python CameraSystemMockerRestApi:"
echo "    $OUTPUT_ROOT/python/CameraSystemMockerRestApi/camera_system_integrator"
echo
echo "  JavaScript client:"
echo "    $OUTPUT_ROOT/javascript/client/CambotApi"
echo "    $OUTPUT_ROOT/javascript/client/CameraSystemIntegrator"
