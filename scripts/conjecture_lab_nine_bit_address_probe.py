#!/usr/bin/env python3
"""Conjecture Lab CL-01: nine-bit class-address lookup (exploratory).

Hypothesis adopted only for this probe: each nine-cell slash/dash class
body is a binary address into an external record collection; the final
three cells choose one of three channels. This is not a validated decoder.

Exact conditional A+B ensemble: body has a 3-of-9 minority and one
minority per physical IAB/CDE/FGH column; Q4 has one slash per depth
stack. Data and generators come from Experiment 450.
"""
import json
from itertools import product
from pathlib import Path

from enumerate_sticker_completion_ensembles import (
    observations, primary_frame_choices, primary_columns, q4_choices,
)

ROOT = Path(__file__).resolve().parents[1]
LETTERS = "ABCDEFGHI"


def class_address_vector(frames, reverse=False, slash_bit=1):
    """A-I native serial class order, nine consecutive primary frames."""
    result = []
    for j in range(9):
        bits = [slash_bit if frame[j] == "/" else 1 - slash_bit
                for frame in frames]
        if reverse:
            bits.reverse()
        result.append(sum(bit << (8 - i) for i, bit in enumerate(bits)))
    return tuple(result)


def build_probe():
    count, observed = observations()
    assert count == 84 and len(observed) == 66, (
        "Observation snapshot changed: do not reuse frozen probe counts")
    choices = [
        [row for row in primary_frame_choices(observed, frame)
         if primary_columns(row)]
        for frame in range(9)
    ]
    primary = list(product(*choices))
    tail_choices = q4_choices(observed)
    tail = list(product(*tail_choices))
    assert len(primary) == 18 and len(tail) == 18
    with (ROOT / "data/terminal41-source-tree.json").open(encoding="utf8") as fh:
        archived = json.load(fh)
    assert archived["count"] == len(archived["files"]) == 74
    schemes = []
    for reverse, slash_bit in product((False, True), (0, 1)):
        vectors = [class_address_vector(fs, reverse, slash_bit)
                   for fs in primary]
        minimum_max = min(max(row) for row in vectors)
        maximum_max = max(max(row) for row in vectors)
        # Zero-based index in a 74-entry table must be in [0,73].
        fit_74 = sum(all(0 <= v < 74 for v in row) for row in vectors)
        schemes.append({
            "direction": "reverse" if reverse else "forward",
            "slash_bit": slash_bit,
            "primary_vectors": len(vectors),
            "full_h108_masters": len(vectors) * len(tail),
            "vectors_all_indices_in_74": fit_74,
            "minimum_of_maximum_class_address": minimum_max,
            "maximum_of_maximum_class_address": maximum_max,
            "minimum_zero_based_table_entries": minimum_max + 1,
            "class_F_addresses": sorted(set(row[5] for row in vectors)),
        })
    assert [(s["direction"], s["slash_bit"],
             s["vectors_all_indices_in_74"],
             s["minimum_zero_based_table_entries"])
            for s in schemes] == [
                ("forward", 0, 0, 454),
                ("forward", 1, 0, 408),
                ("reverse", 0, 0, 328),
                ("reverse", 1, 0, 474),
            ], "Probe census changed"
    native = [class_address_vector(fs) for fs in primary]
    per_class = {
        LETTERS[j]: sorted({row[j] for row in native})
        for j in range(9)
    }
    assert per_class["F"] == [407] and per_class["B"] == [382]
    return {
        "status": "CONDITIONAL EXPLORATORY; not evidence of intended decoder",
        "observations": count,
        "unique_observed_residues": len(observed),
        "body_grammars": len(primary),
        "tail_codes": len(tail),
        "full_masters": len(primary) * len(tail),
        "archive_route_inventory": len(archived["files"]),
        "specifications": schemes,
        "forward_slash_one_address_support": per_class,
        "native_selector_depth_support": {
            LETTERS[j]: tail_choices[j] for j in range(9)
        },
        "scope": (
            "Rejects only direct zero-based nine-address lookup against "
            "the current 74 archived route entries, with the stated "
            "binary polarity and direction choices. The archive is not "
            "a complete proven historical 512-entry record library."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(build_probe(), indent=2))
