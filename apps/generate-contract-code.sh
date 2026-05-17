#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/generate-openapi-code.sh"
"$SCRIPT_DIR/generate-db-code.sh"
