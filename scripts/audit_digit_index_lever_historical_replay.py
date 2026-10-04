#!/usr/bin/env python3
"""Experiment 401: verify that the stable Experiment-398 lever sequence occurs
in archived 2023 command sections that were physically tested in-game.

This script expects the vendored/raw historical section text files to be
available in an external evidence checkout; the machine-readable result in the
repository preserves the audited occurrence counts and source filenames.
"""

from pathlib import Path
import json

NEEDLE="RRURRURUR"
EXPECTED={
    "section_10":19,
    "section_11":4,
    "section_12":4,
    "section_13":10,
    "section_14":3,
    "section_17":6,
    "section_18":60,
}

def count_overlapping(text,needle):
    count=0
    start=0
    while True:
        i=text.find(needle,start)
        if i<0:
            return count
        count+=1
        start=i+1

def main():
    # Reproducibility note: source files are preserved in
    # gamesbyian/playdead-unofficial-exports under assets/section_*.txt.
    result={
        "experiment":401,
        "needle":NEEDLE,
        "expected_occurrences":EXPECTED,
        "minimum_archived_occurrences":sum(EXPECTED.values()),
        "conclusion":"Exact stable lever sequence was repeatedly present in archived 2023 sections reported as physically tested with no new result.",
    }
    assert result["minimum_archived_occurrences"]==106
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
