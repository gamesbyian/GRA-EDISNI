#!/usr/bin/env python3
"""Experiment 337: exact A/B/P loss-map alignment for 534brn captures.

Fetch three preserved captures from a pinned commit of
gamesbyian/playdead-unofficial-exports through GitHub's contents API as base64.
Never decode the source blobs as text.

Normalization is deliberately conservative:
- B/P stored UTF-8 U+FFFD triples become one UNKNOWN token;
- A literal '?' bytes become UNKNOWN tokens because that capture used '?' as
  its lossy replacement representation;
- CR/LF line-wrap bytes are removed from comparison;
- no image bytes are guessed and HTML entities are not decoded.

Pairwise alignments are constrained by unique 12-byte known anchors and solved
between anchors by minimum edit cost. UNKNOWN matches any byte at zero cost;
known mismatch costs 3; insertion/deletion costs 1. This makes known-known
conflict more expensive than representing an inserted/deleted parser byte.
"""

from __future__ import annotations

import base64
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "534brn-loss-map-summary.json"

UPSTREAM_REPO = "gamesbyian/playdead-unofficial-exports"
UPSTREAM_REF = "5e5897e2ce70dad5a2bd85e459770637cb36610f"
PATHS = {
    "A": "assets/534brn9653f9j8mmd_original-4f038b969c841fd7.html",
    "B": "assets/534brn9653f9j8mmd_1-9014735779444bc3.html",
    "P": "assets/message-630970294e9fb0ce.txt",
}
EXPECTED_SHA = {
    "A": "ce55c03ee972954f6e80f55a1a279bb85024f99b",
    "B": "f12c02c49f4c3f7589419fe8e20d655f7b95a9f4",
    "P": "9580913d043ca3efd54a01a38a9cff5767ea8ee7",
}

UNKNOWN = 256
ANCHOR = 12
TERMINAL = b"pe^!02un"


def fetch_blob(path: str) -> tuple[str, bytes]:
    quoted = urllib.parse.quote(path)
    url = (
        f"https://api.github.com/repos/{UPSTREAM_REPO}/contents/{quoted}"
        f"?ref={UPSTREAM_REF}"
    )
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req) as response:
        data = json.load(response)
    return data["sha"], base64.b64decode(data["content"])


def tokenize(blob: bytes, label: str) -> list[int]:
    out: list[int] = []
    i = 0
    while i < len(blob):
        if label in {"B", "P"} and blob[i : i + 3] == b"\xef\xbf\xbd":
            out.append(UNKNOWN)
            i += 3
            continue
        value = blob[i]
        if label == "A" and value == 0x3F:
            out.append(UNKNOWN)
            i += 1
            continue
        if value in (0x0D, 0x0A):
            i += 1
            continue
        out.append(value)
        i += 1
    return out


def find_ascii(tokens: list[int], needle: bytes) -> int:
    target = list(needle)
    for start in range(len(tokens) - len(target) + 1):
        if tokens[start : start + len(target)] == target:
            return start
    raise AssertionError(f"marker not found: {needle!r}")


def known_key(tokens: list[int], start: int, width: int) -> tuple[int, ...] | None:
    chunk = tokens[start : start + width]
    if len(chunk) != width or UNKNOWN in chunk:
        return None
    return tuple(chunk)


def align_gap(left: list[int], right: list[int]) -> list[tuple[int, int]]:
    """Global alignment for one anchor-bounded gap."""
    n, m = len(left), len(right)
    dirs = [bytearray(m + 1) for _ in range(n + 1)]
    prev = list(range(m + 1))
    cur = [0] * (m + 1)
    for j in range(1, m + 1):
        dirs[0][j] = 2  # left

    for i in range(1, n + 1):
        cur[0] = i
        dirs[i][0] = 1  # up
        for j in range(1, m + 1):
            a, b = left[i - 1], right[j - 1]
            mismatch = 0 if a == UNKNOWN or b == UNKNOWN or a == b else 3
            best = prev[j - 1] + mismatch
            direction = 0
            up = prev[j] + 1
            if up < best:
                best, direction = up, 1
            across = cur[j - 1] + 1
            if across < best:
                best, direction = across, 2
            cur[j] = best
            dirs[i][j] = direction
        prev, cur = cur, prev

    i, j = n, m
    pairs: list[tuple[int, int]] = []
    while i or j:
        direction = dirs[i][j]
        if i and j and direction == 0:
            pairs.append((i - 1, j - 1))
            i -= 1
            j -= 1
        elif i and (not j or direction == 1):
            pairs.append((i - 1, -1))
            i -= 1
        else:
            pairs.append((-1, j - 1))
            j -= 1
    pairs.reverse()
    return pairs


def unique_anchors(left: list[int], right: list[int]) -> list[tuple[int, int]]:
    index: dict[tuple[int, ...], list[int]] = {}
    for i in range(len(right) - ANCHOR + 1):
        key = known_key(right, i, ANCHOR)
        if key is not None:
            index.setdefault(key, []).append(i)

    raw: list[tuple[int, int]] = []
    for i in range(len(left) - ANCHOR + 1):
        key = known_key(left, i, ANCHOR)
        if key is None:
            continue
        positions = index.get(key, [])
        if len(positions) == 1:
            raw.append((i, positions[0]))

    anchors: list[tuple[int, int]] = []
    last_left = last_right = -ANCHOR
    for item in raw:
        if item[0] >= last_left + ANCHOR and item[1] >= last_right + ANCHOR:
            anchors.append(item)
            last_left, last_right = item
    return anchors


def make_map(
    left: list[int],
    right: list[int],
    left_start: int,
    left_end: int,
    right_start: int,
    right_end: int,
) -> dict[int, int]:
    """Return right-index -> left-index mapping across a marker-bounded span."""
    ls = left[left_start:left_end]
    rs = right[right_start:right_end]
    anchors = unique_anchors(ls, rs)
    anchors = [
        pair
        for pair in anchors
        if pair[0] + ANCHOR < len(ls) - len(TERMINAL)
        and pair[1] + ANCHOR < len(rs) - len(TERMINAL)
    ]
    anchors.append((len(ls) - len(TERMINAL), len(rs) - len(TERMINAL)))

    mapping: dict[int, int] = {}
    lp = rp = 0
    for la, ra in anchors:
        for li, ri in align_gap(ls[lp:la], rs[rp:ra]):
            if li >= 0 and ri >= 0:
                mapping[right_start + rp + ri] = left_start + lp + li

        take = len(TERMINAL) if la == len(ls) - len(TERMINAL) else ANCHOR
        for offset in range(take):
            mapping[right_start + ra + offset] = left_start + la + offset
        lp, rp = la + take, ra + take
    return mapping


def pair_stats(
    left: list[int],
    right: list[int],
    mapping: dict[int, int],
    right_start: int,
    right_end: int,
) -> dict[str, int]:
    out = {
        "known_equal": 0,
        "known_conflict": 0,
        "left_known_right_unknown": 0,
        "left_unknown_right_known": 0,
        "both_unknown": 0,
    }
    for ri in range(right_start, right_end):
        li = mapping.get(ri)
        if li is None:
            continue
        a, b = left[li], right[ri]
        if a == UNKNOWN and b == UNKNOWN:
            out["both_unknown"] += 1
        elif a == UNKNOWN:
            out["left_unknown_right_known"] += 1
        elif b == UNKNOWN:
            out["left_known_right_unknown"] += 1
        elif a == b:
            out["known_equal"] += 1
        else:
            out["known_conflict"] += 1
    return out


def main() -> None:
    blobs: dict[str, bytes] = {}
    for label, path in PATHS.items():
        sha, blob = fetch_blob(path)
        assert sha == EXPECTED_SHA[label], (label, sha)
        blobs[label] = blob

    tokens = {label: tokenize(blob, label) for label, blob in blobs.items()}
    A, B, P = tokens["A"], tokens["B"], tokens["P"]

    a_jfif = find_ascii(A, b"JFIF")
    b_jfif = find_ascii(B, b"JFIF")
    a_terminal = find_ascii(A, TERMINAL)
    b_terminal = find_ascii(B, TERMINAL)
    p_terminal = find_ascii(P, TERMINAL)

    map_a = make_map(A, B, a_jfif, a_terminal + 8, b_jfif, b_terminal + 8)

    # P lacks the JFIF/EXIF prefix. The earliest unique 12-byte known anchor is
    # P token 2 == B token 7389, fixing a start offset of 7387.
    p_b_start = 7387
    map_p = make_map(P, B, 0, p_terminal + 8, p_b_start, b_terminal + 8)

    ab = pair_stats(A, B, map_a, b_jfif, b_terminal + 8)
    pb = pair_stats(P, B, map_p, p_b_start, b_terminal + 8)

    b_unknown = 0
    recovered_a = 0
    recovered_p = 0
    recovered_union = 0
    both_recover = 0
    both_agree = 0
    both_conflict = 0
    conflict_positions: list[dict[str, int | str]] = []

    for bi in range(b_jfif, b_terminal + 8):
        if B[bi] != UNKNOWN:
            continue
        b_unknown += 1
        ai = map_a.get(bi)
        pi = map_p.get(bi)
        av = A[ai] if ai is not None else UNKNOWN
        pv = P[pi] if pi is not None else UNKNOWN
        a_known = ai is not None and av != UNKNOWN
        p_known = pi is not None and pv != UNKNOWN

        if a_known:
            recovered_a += 1
        if p_known:
            recovered_p += 1
        if a_known or p_known:
            recovered_union += 1
        if a_known and p_known:
            both_recover += 1
            if av == pv:
                both_agree += 1
            else:
                both_conflict += 1
                conflict_positions.append(
                    {
                        "b_token": bi,
                        "b_from_jfif": bi - b_jfif,
                        "a_value_hex": f"{av:02x}",
                        "p_value_hex": f"{pv:02x}",
                    }
                )

    safe_recovered = recovered_union - both_conflict
    remaining_unknown = b_unknown - safe_recovered

    result = {
        "schema_version": 1,
        "experiment": 337,
        "upstream_repository": UPSTREAM_REPO,
        "upstream_commit": UPSTREAM_REF,
        "normalization": {
            "A_question_mark_is_unknown": True,
            "B_P_ufffd_triplet_is_one_unknown": True,
            "remove_cr_lf_for_alignment": True,
            "decode_html_entities": False,
            "guess_image_bytes": False,
        },
        "pairwise": {
            "A_vs_B": ab,
            "P_vs_B": pb,
        },
        "B_payload": {
            "range": "JFIF through pe^!02un",
            "unknown_tokens_before_cross_capture_recovery": b_unknown,
            "B_unknown_recovered_by_A": recovered_a,
            "B_unknown_recovered_by_P": recovered_p,
            "B_unknown_recovered_by_either": recovered_union,
            "B_unknown_recovered_by_both": both_recover,
            "both_known_and_agree": both_agree,
            "both_known_but_conflict": both_conflict,
            "safe_exact_recoveries": safe_recovered,
            "remaining_unknown_after_safe_union": remaining_unknown,
        },
        "conflict_positions": conflict_positions,
        "interpretation": [
            "A and B align from JFIF to terminal with no known-known conflict.",
            "P aligns into B from its earliest unique known anchor through terminal with no known-known conflict.",
            "Cross-capture union supplies 238 safe exact bytes at positions unknown in B.",
            "Ten positions have incompatible known A/P values and remain unknown.",
            "This is a byte-constraint recovery result, not a reconstructed JPEG or inferred pixel result.",
        ],
    }

    assert ab["known_conflict"] == 0
    assert pb["known_conflict"] == 0
    assert recovered_a == 238
    assert recovered_p == 99
    assert recovered_union == 248
    assert both_recover == 89
    assert both_agree == 79
    assert both_conflict == 10
    assert safe_recovered == 238
    assert b_unknown == 1995
    assert remaining_unknown == 1757

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
