#!/usr/bin/env python3
"""Experiment 301: reproduce the historical Discord interval scanner exactly.

The archived C++ program scans offsets 1..299. An offset survives iff:
- at least one observed sticker pair is separated by exactly that offset; and
- every such observed pair has the same foreground symbol.

Its printed "total number of stickers" is not an observation. It is the next
strictly greater multiple of the candidate offset after serial 597, computed by
597 + offset - (597 % offset).

This audit freezes the historical input table and asserts the exact output.
"""

OBS = {
2:1,3:2,20:1,21:2,32:1,37:2,38:1,39:1,47:1,53:2,59:1,63:1,65:1,66:1,72:2,
92:3,95:3,97:3,118:2,123:1,125:1,126:2,132:2,154:1,156:1,164:1,171:1,178:2,
179:2,182:2,183:2,184:1,187:1,193:3,194:1,206:3,221:1,223:1,231:1,242:2,
245:1,247:2,248:1,252:1,258:1,263:1,267:2,282:1,296:1,306:3,312:1,317:1,
324:1,328:2,333:1,334:2,336:2,338:2,339:1,343:2,347:2,354:1,362:1,364:1,
366:1,375:2,384:1,393:1,402:1,405:1,413:3,436:2,444:2,445:1,449:1,450:2,
469:2,470:1,475:1,476:2,478:1,597:2,
}
MAX_SERIAL = 597

def scan_offset(offset):
    match = 0
    for j in range(600):
        k = j + offset
        if k > 599:
            continue
        if j not in OBS or k not in OBS:
            continue
        if OBS[j] != OBS[k]:
            return None
        match += 1
    return match if match else None

def printed_total(offset):
    return MAX_SERIAL + offset - (MAX_SERIAL % offset)

def main():
    survivors = []
    for offset in range(1, 300):
        matches = scan_offset(offset)
        if matches is not None:
            survivors.append((offset, matches, printed_total(offset)))

    expected = [
        (108, 8, 648),
        (125, 7, 625),
        (197, 6, 788),
        (216, 5, 648),
        (254, 4, 762),
    ]
    assert survivors == expected
    assert len(OBS) == 82

    print("offset,matches,printed_total")
    for row in survivors:
        print(",".join(map(str, row)))

    print("\nInterpretation:")
    print("- 108 is the smallest contradiction-free tested offset with any exact-offset support.")
    print("- 216 is automatically compatible with a 108-period object and is not independent confirmation.")
    print("- 125/197/254 survive only because sparse exact-offset comparisons contain no contradiction.")
    print("- printed_total is arithmetic extrapolation to the next multiple after serial 597, not production evidence.")

if __name__ == "__main__":
    main()
