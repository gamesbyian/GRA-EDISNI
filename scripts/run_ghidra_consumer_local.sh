#!/usr/bin/env bash
# Optional native target fallback, requiring user-supplied binary and Ghidra.
set -euo pipefail
if [[ $# -ne 2 ]]; then
  echo 'Usage: GHIDRA_HOME=/path/to/ghidra bash scripts/run_ghidra_consumer_local.sh /path/to/native-binary /path/to/output.csv' >&2
  exit 2
fi
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BINARY="$(realpath -- "$1")"
OUTPUT="$(realpath -m -- "$2")"
if [[ ! -f "$BINARY" ]]; then echo 'Binary not found' >&2; exit 2; fi
if [[ -z "${GHIDRA_HOME:-}" || ! -x "$GHIDRA_HOME/support/analyzeHeadless" ]]; then
  echo 'Set GHIDRA_HOME to a local Ghidra installation with support/analyzeHeadless' >&2; exit 3
fi
mkdir -p -- "$(dirname -- "$OUTPUT")"
TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
sha256sum -- "$BINARY" > "$OUTPUT.input-sha256.txt"
"$GHIDRA_HOME/support/analyzeHeadless" "$TMP" ConsumerLocal \
  -import "$BINARY" -scriptPath "$HERE/ghidra" \
  -postScript InspectConsumerStrings.java "$OUTPUT" \
  -analysisTimeoutPerFile 300 -deleteProject -readOnly
if [[ ! -s "$OUTPUT" ]]; then echo 'Ghidra did not write a report' >&2; exit 4; fi
echo "Local native string triage: $OUTPUT (not a validated decoder)"
