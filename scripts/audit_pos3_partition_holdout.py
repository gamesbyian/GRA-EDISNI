#!/usr/bin/env python3
"""Experiment 265: holdout validation of POS3 rail discovery.

Use the unique 34-residue minimum witness as a discovery/training set, then
reserve the other 20 observed primary H108 residues as holdout evidence.

Search all 280 unlabeled 3+3+3 partitions of the 3x3 physical cells.

Discovery rule on the 34-residue witness:
  1. keep partitions compatible with exact POS3 in all nine frames;
  2. among those, maximize the number of frames whose symbol polarity is
     uniquely forced.

Then reveal the withheld primary observations and ask which nominated
partitions remain compatible in all nine frames.

This separates candidate generation from validation and reduces hindsight.
"""

from __future__ import annotations

from audit_all_pos3_partitions import (
    all_partitions,
    compatible_frames,
    is_vertical_columns,
    partition_label,
)
from audit_pos3_rail_orientation import WITNESS, frame_observations
from enumerate_raw_machine import load_rows


def main() -> None:
    rows = load_rows()
    partitions = tuple(all_partitions())
    assert len(partitions) == 280

    witness_frames = frame_observations(rows, WITNESS)
    full_frames = frame_observations(rows)

    compatible = []
    for partition in partitions:
        frames, forced = compatible_frames(witness_frames, partition)
        if frames == 9:
            compatible.append((partition, forced))

    assert len(compatible) == 168
    max_forced = max(forced for _partition, forced in compatible)
    assert max_forced == 8

    nominees = [
        partition
        for partition, forced in compatible
        if forced == max_forced
    ]
    assert len(nominees) == 5

    expected_nominee_labels = sorted([
        "ICF/ADG/BEH",
        "IDG/ABE/CFH",
        "IDG/ACF/BEH",
        "IDH/ABE/CFG",
        "IDH/ACF/BEG",
    ])
    assert sorted(partition_label(partition) for partition in nominees) == expected_nominee_labels

    validated = []
    validation_scores = {}
    for partition in nominees:
        frames, forced = compatible_frames(full_frames, partition)
        validation_scores[partition_label(partition)] = (frames, forced)
        if frames == 9:
            validated.append(partition)

    assert len(validated) == 1
    assert is_vertical_columns(validated[0])
    assert partition_label(validated[0]) == "ICF/ADG/BEH"

    assert validation_scores == {
        "ICF/ADG/BEH": (9, 8),
        "IDG/ABE/CFH": (4, 4),
        "IDG/ACF/BEH": (6, 6),
        "IDH/ABE/CFG": (5, 5),
        "IDH/ACF/BEG": (4, 4),
    }

    primary_residues = {
        int(record["residue"])
        for record in rows
        if int(record["residue"]) <= 81
    }
    assert len(primary_residues) == 54
    assert len(WITNESS) == 34
    assert len(primary_residues - WITNESS) == 20

    print("Experiment 265")
    print("discovery set: 34 primary residues")
    print("holdout set:", len(primary_residues - WITNESS), "primary residues")
    print("all rail partitions:", len(partitions))
    print("witness-compatible across all 9 frames:", len(compatible))
    print("maximum witness polarity determinacy:", max_forced, "/ 9")
    print("max-determinacy nominees:", len(nominees))
    for label in expected_nominee_labels:
        print(" ", label, "-> full corpus", validation_scores[label])
    print("RESULT: only physical columns survive the withheld observations")
    print("RESULT: column POS3 can be selected by witness discovery + independent holdout validation")


if __name__ == "__main__":
    main()
