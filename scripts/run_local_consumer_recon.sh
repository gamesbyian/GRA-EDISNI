#!/usr/bin/env bash
# Only locally supplied installed game bytes. No uploads or third-party calls.
set -euo pipefail
if [[ $# -ne 2 ]]; then
  echo 'Usage: bash scripts/run_local_consumer_recon.sh /path/to/INSIDE-install /path/to/output' >&2
  exit 2
fi
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL="$(cd -- "$1" && pwd)"
mkdir -p -- "$2"
OUT="$(cd -- "$2" && pwd)"
if [[ "$OUT" == "$INSTALL" || "$OUT" == "$INSTALL/"* ]]; then
  echo 'Output must be outside the game installation' >&2; exit 2
fi
python3 "$ROOT/scripts/consumer_binary_intake.py" --root "$INSTALL" --output "$OUT/intake.json"
export CONSUMER_INTAKE_JSON="$OUT/intake.json"
ASSEMBLY_REL="$(python3 - <<'PY'
import json,os
p=json.load(open(os.environ['CONSUMER_INTAKE_JSON'],encoding='utf-8'))
x=[v['relative_path'] for v in p['files'] if v['role']=='gameplay-managed-candidate' and v['header_kind']=='pe-cli-managed']
if len(x)!=1:
    raise SystemExit(f'Expected exactly one verified managed Assembly-CSharp.dll; found {len(x)}. Review intake.json.')
print(x[0])
PY
)"
if ! command -v ilspycmd >/dev/null; then
  echo 'ilspycmd is not installed. Install it from icsharpcode/ILSpy and rerun.' >&2; exit 3
fi
mkdir -p "$OUT/decompiled"
ilspycmd -p -o "$OUT/decompiled" "$INSTALL/$ASSEMBLY_REL"
python3 "$ROOT/scripts/audit_decompiled_consumer_hits.py" --source-dir "$OUT/decompiled" --output "$OUT/candidate-hits.json"
echo "Produced local intake.json, candidate-hits.json and decompiled source in $OUT"
