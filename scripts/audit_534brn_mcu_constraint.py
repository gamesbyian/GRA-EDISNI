#!/usr/bin/env python3
"""Experiment 423: bounded JPEG entropy/MCU-count constraint decoder.

This does NOT reconstruct pixels or choose values for damaged bytes.

It consumes the P capture under the same lossy-token model as Experiments
316/337/417, uses the standard baseline JPEG Huffman tables visibly preserved
by the capture, and propagates all byte possibilities compatible with the
text-loss channel.  The only semantic output is the set of feasible complete
MCU counts at the EOI boundary.

Model:
- U+FFFD in P represents one lost original byte in 0x80..0xFF.
- ASCII bytes are preserved exactly, except space 0x20 may also represent
  original NUL 0x00 under the documented NUL->space text transform.
- CR/LF wrapper line breaks are removed, matching the prior normalized stream.
- entropy byte 0xFF requires a following stuffed 0x00 token.
- no restart markers are admitted (Experiment 417 found no DRI segment).
- coefficients/amplitudes are never reconstructed; amplitude bits are simply
  consumed.
"""

from __future__ import annotations

import base64
import json
import urllib.parse
import urllib.request
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-423-534brn-mcu-constraint.json"

UPSTREAM_REPO = "gamesbyian/playdead-unofficial-exports"
UPSTREAM_REF = "5e5897e2ce70dad5a2bd85e459770637cb36610f"
P_PATH = "assets/message-630970294e9fb0ce.txt"

UNKNOWN = 256
FOOTER = b"pe^!02un"
MAX_MCU = 300

# JPEG Annex K / libjpeg standard tables.
BITS_DC_L = [0, 0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
VAL_DC_L = list(range(12))
BITS_DC_C = [0, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
VAL_DC_C = list(range(12))

BITS_AC_L = [0, 0, 2, 1, 3, 3, 2, 4, 3, 5, 5, 4, 4, 0, 0, 1, 0x7D]
VAL_AC_L = [
    0x01,0x02,0x03,0x00,0x04,0x11,0x05,0x12,
    0x21,0x31,0x41,0x06,0x13,0x51,0x61,0x07,
    0x22,0x71,0x14,0x32,0x81,0x91,0xA1,0x08,
    0x23,0x42,0xB1,0xC1,0x15,0x52,0xD1,0xF0,
    0x24,0x33,0x62,0x72,0x82,0x09,0x0A,0x16,
    0x17,0x18,0x19,0x1A,0x25,0x26,0x27,0x28,
    0x29,0x2A,0x34,0x35,0x36,0x37,0x38,0x39,
    0x3A,0x43,0x44,0x45,0x46,0x47,0x48,0x49,
    0x4A,0x53,0x54,0x55,0x56,0x57,0x58,0x59,
    0x5A,0x63,0x64,0x65,0x66,0x67,0x68,0x69,
    0x6A,0x73,0x74,0x75,0x76,0x77,0x78,0x79,
    0x7A,0x83,0x84,0x85,0x86,0x87,0x88,0x89,
    0x8A,0x92,0x93,0x94,0x95,0x96,0x97,0x98,
    0x99,0x9A,0xA2,0xA3,0xA4,0xA5,0xA6,0xA7,
    0xA8,0xA9,0xAA,0xB2,0xB3,0xB4,0xB5,0xB6,
    0xB7,0xB8,0xB9,0xBA,0xC2,0xC3,0xC4,0xC5,
    0xC6,0xC7,0xC8,0xC9,0xCA,0xD2,0xD3,0xD4,
    0xD5,0xD6,0xD7,0xD8,0xD9,0xDA,0xE1,0xE2,
    0xE3,0xE4,0xE5,0xE6,0xE7,0xE8,0xE9,0xEA,
    0xF1,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,
    0xF9,0xFA,
]
BITS_AC_C = [0, 0, 2, 1, 2, 4, 4, 3, 4, 7, 5, 4, 4, 0, 1, 2, 0x77]
VAL_AC_C = [
    0x00,0x01,0x02,0x03,0x11,0x04,0x05,0x21,
    0x31,0x06,0x12,0x41,0x51,0x07,0x61,0x71,
    0x13,0x22,0x32,0x81,0x08,0x14,0x42,0x91,
    0xA1,0xB1,0xC1,0x09,0x23,0x33,0x52,0xF0,
    0x15,0x62,0x72,0xD1,0x0A,0x16,0x24,0x34,
    0xE1,0x25,0xF1,0x17,0x18,0x19,0x1A,0x26,
    0x27,0x28,0x29,0x2A,0x35,0x36,0x37,0x38,
    0x39,0x3A,0x43,0x44,0x45,0x46,0x47,0x48,
    0x49,0x4A,0x53,0x54,0x55,0x56,0x57,0x58,
    0x59,0x5A,0x63,0x64,0x65,0x66,0x67,0x68,
    0x69,0x6A,0x73,0x74,0x75,0x76,0x77,0x78,
    0x79,0x7A,0x82,0x83,0x84,0x85,0x86,0x87,
    0x88,0x89,0x8A,0x92,0x93,0x94,0x95,0x96,
    0x97,0x98,0x99,0x9A,0xA2,0xA3,0xA4,0xA5,
    0xA6,0xA7,0xA8,0xA9,0xAA,0xB2,0xB3,0xB4,
    0xB5,0xB6,0xB7,0xB8,0xB9,0xBA,0xC2,0xC3,
    0xC4,0xC5,0xC6,0xC7,0xC8,0xC9,0xCA,0xD2,
    0xD3,0xD4,0xD5,0xD6,0xD7,0xD8,0xD9,0xDA,
    0xE2,0xE3,0xE4,0xE5,0xE6,0xE7,0xE8,0xE9,
    0xEA,0xF2,0xF3,0xF4,0xF5,0xF6,0xF7,0xF8,
    0xF9,0xFA,
]

def fetch(path: str) -> bytes:
    q = urllib.parse.quote(path)
    u = f"https://api.github.com/repos/{UPSTREAM_REPO}/contents/{q}?ref={UPSTREAM_REF}"
    req = urllib.request.Request(u, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req) as rsp:
        d = json.load(rsp)
    return base64.b64decode(d["content"])

def tokenize_p(blob: bytes) -> list[int]:
    out = []
    i = 0
    while i < len(blob):
        if blob[i:i+3] == b"\xef\xbf\xbd":
            out.append(UNKNOWN)
            i += 3
            continue
        v = blob[i]
        i += 1
        if v in (0x0D, 0x0A):
            continue
        out.append(v)
    return out

def find_seq(tokens, seq):
    seq = list(seq)
    return [i for i in range(len(tokens)-len(seq)+1) if tokens[i:i+len(seq)] == seq]

def find_sos(tokens):
    pat = [UNKNOWN,UNKNOWN,0x20,0x0C,0x03,0x01,0x20,0x02,0x11,0x03,0x11,0x20,0x3F,0x20]
    hits = find_seq(tokens, pat)
    assert hits == [580]
    return hits[0] + len(pat)

class HuffTree:
    def __init__(self, bits, vals):
        self.children = {}
        self.leaf = {}
        self._new_node()
        code = 0
        p = 0
        for length in range(1, 17):
            for _ in range(bits[length]):
                node = 0
                for shift in range(length - 1, -1, -1):
                    bit = (code >> shift) & 1
                    key = (node, bit)
                    if shift == 0:
                        leaf_node = self._new_node()
                        self.children[key] = leaf_node
                        self.leaf[leaf_node] = vals[p]
                        p += 1
                    else:
                        if key not in self.children:
                            self.children[key] = self._new_node()
                        node = self.children[key]
                code += 1
            code <<= 1
        assert p == len(vals)

    def _new_node(self):
        n = len(getattr(self, "nodes", []))
        if not hasattr(self, "nodes"):
            self.nodes = []
        self.nodes.append(n)
        return n

DC_L = HuffTree(BITS_DC_L, VAL_DC_L)
DC_C = HuffTree(BITS_DC_C, VAL_DC_C)
AC_L = HuffTree(BITS_AC_L, VAL_AC_L)
AC_C = HuffTree(BITS_AC_C, VAL_AC_C)

# state tuple:
# (phase, component, k, node, skip)
# phase 0 DC huff, 1 DC amplitude, 2 AC huff, 3 AC amplitude
START = (0, 0, 0, 0, 0)

def is_mcu_boundary(state):
    return state == START

def table_for(phase, comp):
    lum = comp < 4
    if phase == 0:
        return DC_L if lum else DC_C
    return AC_L if lum else AC_C

def finish_block(comp):
    comp += 1
    if comp == 6:
        return START, 1
    return (0, comp, 0, 0, 0), 0

def step_bit(state, bit):
    phase, comp, k, node, skip = state
    if phase in (1, 3):
        skip -= 1
        if skip:
            return (phase, comp, k, node, skip), 0
        if phase == 1:
            return (2, comp, 1, 0, 0), 0
        if k == 64:
            return finish_block(comp)
        return (2, comp, k, 0, 0), 0

    tree = table_for(phase, comp)
    child = tree.children.get((node, bit))
    if child is None:
        return None
    if child not in tree.leaf:
        return (phase, comp, k, child, 0), 0

    sym = tree.leaf[child]
    if phase == 0:
        if not 0 <= sym <= 11:
            return None
        if sym == 0:
            return (2, comp, 1, 0, 0), 0
        return (1, comp, 0, 0, sym), 0

    # AC
    if sym == 0x00:
        return finish_block(comp)
    if sym == 0xF0:
        nk = k + 16
        if nk > 64:
            return None
        if nk == 64:
            return finish_block(comp)
        return (2, comp, nk, 0, 0), 0

    run, size = sym >> 4, sym & 0x0F
    if size == 0:
        return None
    target = k + run
    if target > 63:
        return None
    nk = target + 1
    return (3, comp, nk, 0, size), 0

@lru_cache(maxsize=None)
def byte_transition(state, value):
    cur = state
    delta = 0
    terminal = set()
    for pos in range(8):
        bit = (value >> (7 - pos)) & 1
        stepped = step_bit(cur, bit)
        if stepped is None:
            return None, frozenset(terminal)
        cur, inc = stepped
        delta += inc
        if is_mcu_boundary(cur):
            remaining = 7 - pos
            if remaining == 0:
                terminal.add(delta)
            else:
                mask = (1 << remaining) - 1
                if (value & mask) == mask:
                    terminal.add(delta)
    return (cur, delta), frozenset(terminal)

@lru_cache(maxsize=None)
def domain_transition(state, kind):
    if kind == "unknown_nonff":
        values = range(0x80, 0xFF)
    elif kind == "space":
        values = (0x00, 0x20)
    else:
        values = (kind,)

    outs = set()
    terms = set()
    for value in values:
        out, term = byte_transition(state, value)
        if out is not None:
            outs.add(out)
        terms.update(term)
    return tuple(outs), tuple(sorted(terms))

def add_bits(dst, state, bits):
    if not bits:
        return
    dst[state] = dst.get(state, 0) | bits

def shift_counts(bits, delta):
    return (bits << delta) & ((1 << (MAX_MCU + 1)) - 1)

def terminal_counts(bits, deltas):
    out = 0
    for d in deltas:
        out |= shift_counts(bits, d)
    return out

def decode_feasible_mcus(entropy):
    n = len(entropy)
    frontier = [dict() for _ in range(n + 1)]
    frontier[0][START] = 1  # bit 0 => zero completed MCUs
    accepted = 0
    peak_states = 1

    for i in range(n):
        if not frontier[i]:
            continue
        token = entropy[i]
        next_maps = []

        if token == UNKNOWN:
            # non-FF high byte branch
            next_maps.append((i + 1, "unknown_nonff"))
            # FF data byte must consume one following stuffed zero token
            if i + 1 < n and entropy[i + 1] == 0x20:
                next_maps.append((i + 2, 0xFF))
        elif token == 0x20:
            next_maps.append((i + 1, "space"))
        else:
            next_maps.append((i + 1, token))

        for state, bits in list(frontier[i].items()):
            for ni, kind in next_maps:
                outs, terms = domain_transition(state, kind)
                if ni == n:
                    accepted |= terminal_counts(bits, terms)
                    for ns, delta in outs:
                        if is_mcu_boundary(ns):
                            accepted |= shift_counts(bits, delta)
                else:
                    for ns, delta in outs:
                        add_bits(frontier[ni], ns, shift_counts(bits, delta))

        frontier[i].clear()
        peak_states = max(peak_states, *(len(x) for x in frontier[max(0,i-1):min(n+1,i+3)]))

    return [i for i in range(MAX_MCU + 1) if (accepted >> i) & 1], peak_states

def main():
    tokens = tokenize_p(fetch(P_PATH))
    start = find_sos(tokens)
    footer = find_seq(tokens, FOOTER)
    assert footer == [4752]
    end = footer[0] - 2
    assert tokens[end:footer[0]] == [UNKNOWN, UNKNOWN]
    entropy = tokens[start:end]
    assert len(entropy) == 4156

    feasible, peak_states = decode_feasible_mcus(entropy)

    dimension_counts = {
        m: [
            [w,h]
            for w in range(128,256)
            for h in range(128,256)
            if ((w+15)//16) * ((h+15)//16) == m
        ]
        for m in feasible
        if 64 <= m <= 256
    }
    geometric = sorted(dimension_counts)
    unique_dimension_counts = {
        str(m): dims for m,dims in dimension_counts.items() if len(dims) <= 8
    }

    result = {
        "experiment": 423,
        "capture": "P",
        "entropy_token_span": len(entropy),
        "decoder_model": {
            "huffman_tables": "JPEG Annex K standard baseline tables; capture DHT material matches this family",
            "scan_components": "Y 2x2 + Cb 1x1 + Cr 1x1 => 6 blocks/MCU",
            "replacement_domain": "each U+FFFD token is one original byte 0x80..0xFF",
            "space_domain": "0x20 token may represent original 0x00 or 0x20",
            "byte_stuffing": "0xFF entropy byte requires following 0x00 token",
            "pixels_reconstructed": False,
            "coefficient_values_reconstructed": False,
        },
        "feasible_complete_mcu_counts_0_300": feasible,
        "feasible_mcu_counts_compatible_with_128_255_dimensions": geometric,
        "feasible_count_total": len(feasible),
        "geometric_feasible_count_total": len(geometric),
        "contains_64": 64 in feasible,
        "only_64_in_dimension_domain": geometric == [64],
        "small_dimension_solution_sets": unique_dimension_counts,
        "peak_local_decoder_states": peak_states,
    }

    if geometric == [64]:
        result["conclusion"] = (
            "Under the declared loss channel and standard baseline Huffman tables, the damaged entropy stream "
            "permits exactly 64 MCUs within the independently established 128..255 dimension domain. Combined "
            "with 16x16 MCUs, this uniquely proves 128x128."
        )
    elif 64 not in geometric:
        result["conclusion"] = (
            "The exact constraint decoder excludes 64 MCUs under the declared model, so the 128x128 hypothesis "
            "fails this entropy-structure test."
        )
    else:
        result["conclusion"] = (
            "64 MCUs remains feasible, but other MCU counts compatible with the 128..255 dimension domain also "
            "survive. The entropy structure therefore does not uniquely prove 128x128 from the surviving lossy "
            "capture; the 64-MCU clue remains suggestive rather than established."
        )

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
