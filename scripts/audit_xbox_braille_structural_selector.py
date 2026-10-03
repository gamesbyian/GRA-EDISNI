#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-371-xbox-braille-structural-selector.json"

ROWS = [
    "9N879763","087E894W26","09817986469","PL663AN79ET",
    "976828'9126","7DI89829812","!CO792412-","984VE3229","679RED6",
]

MASK = {
    "!":"011101","'":"001000","-":"001001",
    "0":"001011","1":"010000","2":"011000","3":"010010","4":"010011",
    "5":"010001","6":"011010","7":"011011","8":"011001","9":"001010",
    "A":"100000","C":"100100","D":"100110","E":"100010","I":"010100",
    "L":"111000","N":"101110","O":"101010","P":"111100","R":"111010",
    "T":"011110","V":"111001","W":"010111",
}

TOP_EMPTY = {
    "000000":"space","000001":",","000010":"double_quote","000011":";",
    "001000":"'","001001":"-","001010":"9","001011":"0",
    "010000":"1","010001":"5","010010":"3","010011":"4",
    "011000":"2","011001":"8","011010":"6","011011":"7",
}

def top_active(mask):
    return mask[0] == "1" or mask[3] == "1"

stream = "".join(ROWS)
active = [c for c in stream if top_active(MASK[c])]
inactive = [c for c in stream if not top_active(MASK[c])]
observed_masks = sorted({MASK[c] for c in inactive})
absent_masks = sorted(set(TOP_EMPTY) - set(observed_masks))

result = {
    "experiment": 371,
    "total_cells": len(stream),
    "top_active_cells": len(active),
    "top_empty_cells": len(inactive),
    "top_active_readout": "".join(active),
    "top_active_corrected": "".join(active).replace("!", "S"),
    "top_active_unique_chars": "".join(sorted(set(active))),
    "top_empty_unique_chars": "".join(sorted(set(inactive))),
    "top_empty_possible_patterns": 16,
    "top_empty_observed_patterns": len(observed_masks),
    "top_empty_absent_masks": absent_masks,
    "top_empty_absent_ascii": [TOP_EMPTY[m] for m in absent_masks],
}

assert result["top_active_cells"] == 19
assert result["top_active_corrected"] == "NEWPLANETDISCOVERED"
assert all(c.isalpha() or c == "!" for c in active)
assert all(not c.isalpha() for c in inactive)
assert result["top_empty_observed_patterns"] == 11

OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
