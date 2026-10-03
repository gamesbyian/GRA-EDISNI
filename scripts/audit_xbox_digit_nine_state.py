#!/usr/bin/env python3
"""Experiment 368: audit the residual Braille-ASCII digit alphabet in the Xbox printer solution."""

from collections import Counter
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-368-xbox-digit-nine-state-audit.json"

ROWS = [
    "9N879763",
    "087E894W26",
    "09817986469",
    "PL663AN79ET",
    "976828'9126",
    "7DI89829812",
    "!CO792412-",
    "984VE3229",
    "679RED6",
]

DIGIT_ALPHABET = "0123456789"
CE_CLASSES = "ABCDEFGHI"


def main() -> None:
    cells = "".join(ROWS)
    digits = [c for c in cells if c.isdigit()]
    digit_counts = Counter(digits)
    observed_digits = "".join(d for d in DIGIT_ALPHABET if digit_counts[d])
    missing_digits = "".join(d for d in DIGIT_ALPHABET if not digit_counts[d])

    # These are descriptive nulls only. The Braille cells are spatially generated
    # and are not claimed to be iid decimal draws.
    n = len(digits)
    p_specific_absent_iid_uniform = (9 / 10) ** n
    p_any_digit_absent_iid_uniform = sum(
        (-1) ** (k + 1) * math.comb(10, k) * ((10 - k) / 10) ** n
        for k in range(1, 11)
    )

    # The CE background channel is a deterministic 9-state cycle by sticker serial.
    # Verify that against the physical observation ledger rather than assuming it.
    observations_path = ROOT / "data" / "observations.csv"
    rows = observations_path.read_text(encoding="utf-8").splitlines()[1:]
    checked = 0
    mismatches = []
    for line in rows:
        if not line.strip():
            continue
        serial, residue, symbol, image_class = line.split(",")
        residue_i = int(residue)
        expected = CE_CLASSES[(residue_i - 1) % 9]
        checked += 1
        if image_class != expected:
            mismatches.append(
                {"serial": int(serial), "residue": residue_i, "actual": image_class, "expected": expected}
            )

    result = {
        "experiment": 368,
        "source_transcription": "data/printer-reference/metadata.json:xbox_one.documented_braille_transcription",
        "braille_rows": ROWS,
        "row_lengths": [len(r) for r in ROWS],
        "total_transcribed_cells": len(cells),
        "digit_cells": n,
        "digit_counts": {d: digit_counts[d] for d in DIGIT_ALPHABET},
        "observed_digit_alphabet": observed_digits,
        "missing_digit_alphabet": missing_digits,
        "distinct_observed_digits": len(observed_digits),
        "ce_background_states": len(CE_CLASSES),
        "ce_observation_rows_checked": checked,
        "ce_serial_to_class_mismatches": mismatches,
        "iid_uniform_decimal_descriptive_null": {
            "p_specific_digit_absent_over_67_draws": p_specific_absent_iid_uniform,
            "p_at_least_one_of_10_digits_absent_over_67_draws": p_any_digit_absent_iid_uniform,
            "warning": "Not an inferential p-value: the Xbox characters are spatially generated Braille-ASCII cells, not established iid decimal draws.",
        },
        "mapping_space_size_9_to_9": math.factorial(9),
        "mapping_status": (
            "A bijection between the nine observed Xbox digit glyphs and A-I has 9! = 362880 possibilities, "
            "but there is currently no independently defined Xbox-cell-to-CE-sticker pairing. Therefore exhaustive "
            "enumeration would be unfalsifiable relabeling, not a valid cross-puzzle test."
        ),
        "interpretation": (
            "The missing 5 is a real structural observation: the Xbox residual transcription uses exactly nine of the "
            "ten decimal ASCII glyphs, matching the cardinality of the CE A-I background alphabet. This licenses a "
            "bounded historical-design analogy, but not a direct mapping. A direct transfer test requires an independent "
            "alignment, ordering rule, or shared consumer."
        ),
    }

    if missing_digits != "5":
        raise SystemExit(f"expected only digit 5 to be absent, got {missing_digits!r}")
    if len(observed_digits) != 9:
        raise SystemExit(f"expected nine observed digits, got {observed_digits!r}")
    if mismatches:
        raise SystemExit(f"CE serial→A-I recurrence mismatch: {mismatches}")

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
