#!/usr/bin/env python3
"""Raw-observation variable-width / instruction-grammar investigation.

No incumbent machine, model completions or inferred unknown sticker is imported.
A successful parse is an existence demonstration, NOT evidence of authorship.
Run: python scripts/conjecture_lab_variable_length_grammar.py --observations data/observations.csv --output data/conjecture-lab-variable-length-grammar-2026-10-12.json
"""
from __future__ import annotations

import argparse
import itertools
import csv
import json
import math
import random
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path


ZONES = ((1, 81, "body", "-/"), (82, 108, "tail", "./"))
WIDTHS = (2, 3, 4, 5, 6, 7, 8, 9, 12)
# Two deterministic invented languages. Each codebook is prefix-free.
# Tokens consuming operands of 3 / 5 sites are distinguished from instructions
# applying to the PREVIOUS operand; "skip" consumes a NEXT operand.
CODEBOOKS = {
    "two_bit_backward": {"00": ("emit", 3), "01": ("emit", 5), "10": ("repeat", 0), "11": ("reverse", 0)},
    "two_bit_forward": {"00": ("emit", 3), "01": ("emit", 5), "10": ("skip", 3), "11": ("skip", 5)},
    "prefix_backward": {"0": ("emit", 3), "10": ("emit", 5), "110": ("repeat", 0), "111": ("reverse", 0)},
    "prefix_forward": {"0": ("emit", 3), "10": ("emit", 5), "110": ("skip", 3), "111": ("skip", 5)},
    "two_bit_terminated": {"00": ("emit", 3), "01": ("emit", 5), "10": ("repeat", 0), "11": ("stop", 0)},
    "prefix_terminated": {"0": ("emit", 3), "10": ("emit", 5), "110": ("repeat", 0), "111": ("stop", 0)},
}


def load_observations(path: Path):
    by_residue = {}
    with path.open(newline="", encoding="utf-8") as f:
        records = list(csv.DictReader(f))
    for row in records:
        r, serial, symbol = int(row["residue"]), int(row["serial"]), row["symbol"]
        if not (1 <= r <= 108) or serial % 108 != r % 108:
            raise ValueError("bad serial/residue: " + str(row))
        valid = "-/" if r <= 81 else "./"
        if symbol not in valid:
            raise ValueError("illegal symbol for zone: " + str(row))
        if r in by_residue and by_residue[r] != symbol:
            raise ValueError("conflicting physical observations at " + str(r))
        by_residue[r] = symbol
    return "".join(by_residue.get(i, "?") for i in range(1, 109)), len(records)


def bit_string(physical: str, zero: str, one: str):
    if zero == one:
        raise ValueError("nonbijective bit encoding")
    return "".join("?" if c == "?" else ("0" if c == zero else "1") for c in physical)


def mixed_width_partitions(n: int, widths=(3,5)):
    """All compositions of total length n by widths, without examining marks.

    The count is the multinomial number of distinct width *orderings*, not
    codewords. For (3,5), each tuple gives (#triples,#quintets,count).
    """
    assert widths == (3,5) and n >= 0
    ans=[]
    for quintets in range(n//5+1):
        remainder=n-5*quintets
        if remainder % 3==0:
            triples=remainder//3
            ans.append({"triples":triples,"quintets":quintets,
                        "ordered_partitions":math.comb(triples+quintets,quintets)})
    return {"total_sites":n,"possible_mixtures":ans,
            "ordered_partitions_total":sum(p["ordered_partitions"] for p in ans)}


def fixed_groups(s: str):
    out = {}
    for w in WIDTHS:
        # phases are different alignments, not identical runs of padding.
        phases = []
        for shift in range(w):
            blocks = [s[i:i+w] for i in range(shift, len(s)-w+1, w)]
            known = [p for p in blocks if "?" not in p]
            phases.append({"phase": shift, "whole_blocks": len(blocks), "fully_observed": len(known),
                           "distinct_fully_observed": len(set(known)), "repeated_fully_observed": len(known)-len(set(known))})
        out[str(w)] = phases
    return out


def contiguous_observation(s: str):
    pairs = [(a, b) for a, b in zip(s, s[1:]) if a != "?" and b != "?"]
    triples = [s[i:i+3] for i in range(len(s)-2) if "?" not in s[i:i+3]]
    runs = []
    for k in range(1, 13):
        # "certified" run must be bracketed by a known opposite mark or zone edge.
        certain = []
        for i in range(len(s) - k + 1):
            ss = s[i:i+k]
            if len(set(ss)) != 1 or ss[0] == "?":
                continue
            if (i == 0 or (s[i-1] != "?" and s[i-1] != ss[0])) and (i+k == len(s) or (s[i+k] != "?" and s[i+k] != ss[0])):
                certain.append(i+1)
        if certain:
            runs.append({"length":k,"starts_zone_relative":certain})
    return {"known_adjacent_pairs":len(pairs),"matching_pairs":sum(a==b for a,b in pairs),
            "mismatching_pairs":sum(a!=b for a,b in pairs),"fully_observed_triples":len(triples),
            "triple_counts":dict(sorted(Counter(triples).items())),"certified_maximal_runs":runs}


def completed_runs(s: str, target_length: int):
    """Exact min/max count of maximal runs of a chosen length over 2^missing fills.

    State (last bit, last-run length capped at k+1). Closing a run counts
    iff its length is exactly k; final run also closes at zone end.
    """
    k = target_length
    state = {(None, 0): (0, 0)}
    for c in s:
        ns = {}
        for (last, l), (lo, hi) in state.items():
            for bit in ("0", "1") if c == "?" else (c,):
                close = int(last is not None and last != bit and l == k)
                nl = min(l+1, k+1) if last == bit else 1
                key = (bit, nl)
                old = ns.get(key, (math.inf, -math.inf))
                ns[key] = (min(old[0], lo+close), max(old[1], hi+close))
        state = ns
    return [min(lo + (l == k) for (last, l), (lo, hi) in state.items()),
            max(hi + (l == k) for (last, l), (lo, hi) in state.items())]


def is_prefix_free(codebook):
    words = sorted(codebook)
    return all(not b.startswith(a) for i,a in enumerate(words) for b in words[i+1:])


def matches(partial, known):
    return len(partial)==len(known) and all(a=="?" or a==b for a,b in zip(partial,known))


def execute_complete_program(bits: str, codebook):
    """Execute a fully assigned *invented* instruction grammar.

    A backward command repeats or reverses the most recent emitted CHUNK;
    a forward command skips (consumes without emitting) the next 3/5 bits.
    No meaning is assigned to resulting bit strings or byte values.
    """
    assert is_prefix_free(codebook) and "?" not in bits
    pos, last, emitted, actions, stopped = 0, None, [], [], False
    needs_stop = any(op == "stop" for op,_ in codebook.values())
    while pos < len(bits):
        found = [key for key in codebook if bits.startswith(key, pos)]
        if len(found) != 1:
            return None
        key = found[0]
        op, width = codebook[key]
        start = pos
        pos += len(key)
        if pos+width > len(bits):
            return None
        operand = bits[pos:pos+width]
        pos += width
        if op == "emit":
            last = operand
            emitted.append(operand)
        elif op == "repeat":
            if last is None: return None
            emitted.append(last)
        elif op == "reverse":
            if last is None: return None
            last = last[::-1]
            emitted.append(last)
        elif op == "skip":
            pass
        elif op == "stop":
            if last is None or pos != len(bits): return None
            stopped = True
        else:
            raise ValueError(op)
        actions.append({"start":start,"op":op,"operand":operand})
    if needs_stop and not stopped:
        return None
    return {"actions":actions,"emitted_chunks":emitted,"output":"".join(emitted)}


def parse_program(partial: str, codebook):
    """Exact number of full missing-bit assignments giving valid deterministic parse.

    Operands are opaque bits; repeat/reverse require a previous emitted operand;
    STOP, if present in the codebook, must occur only at the actual zone end.
    Every codebook is prefix-free, so no completed string has multiple parses.
    """
    assert is_prefix_free(codebook)
    n = len(partial)
    requires_stop = any(op == "stop" for op, _ in codebook.values())
    @lru_cache(None)
    def dp(pos, has_previous, used_control, require_control):
        if pos == n:
            return int(not requires_stop and (used_control or not require_control))
        total = 0
        for token, (op, width) in codebook.items():
            end = pos + len(token) + width
            if end > n or not matches(partial[pos:pos+len(token)], token):
                continue
            if op in ("repeat", "reverse") and not has_previous:
                continue
            if op == "stop":
                if end == n and has_previous and (used_control or not require_control):
                    total += 1
                continue
            remaining = partial[pos+len(token):end]
            control = op in ("repeat", "reverse", "skip")
            total += (1 << remaining.count("?")) * dp(
                end, has_previous or op == "emit", used_control or control, require_control)
        return total
    total = dp(0, False, False, False)
    with_control = dp(0, False, False, True)
    assert with_control <= total
    cursor, seen, used, trace, example = 0, False, False, [], []
    while total and cursor < n:
        found = False
        for token in sorted(codebook):
            op, width = codebook[token]
            end = cursor + len(token) + width
            if end > n or not matches(partial[cursor:cursor+len(token)], token):
                continue
            if op in ("repeat", "reverse") and not seen:
                continue
            if op == "stop":
                continuation = int(end == n and seen)
            else:
                continuation = dp(end, seen or op == "emit",
                                  used or op in ("repeat", "reverse", "skip"), False)
            if continuation == 0:
                continue
            argument = partial[cursor+len(token):end].replace("?", "0")
            example.extend([*token, *argument])
            trace.append({"at": cursor, "opcode": token, "action": op, "argument": argument})
            seen = seen or op == "emit"
            used = used or op in ("repeat", "reverse", "skip")
            cursor = end
            found = True
            break
        assert found, "DP and witness disagree"
    assert cursor == n or total == 0
    possible = 1 << partial.count("?")
    assert total <= possible, "a binary completion received multiple parses"
    return {"program_completions":total,"with_control_completions":with_control,
            "possible_completions":possible,"accepted_fraction":f"{total}/{possible}",
            "example_trace":trace[:12],"example_completed_bits":"".join(example) if total else None,
            "example_output":execute_complete_program("".join(example),codebook)["output"] if total else None}


def exact_markov_transitions(s: str):
    # Min/max transitions over all complete binary fills (raw observation only).
    states = {None: (0, 0)}
    for c in s:
        nexts = {}
        for last,(lo,hi) in states.items():
            for bit in ("0", "1") if c == "?" else (c,):
                incr = int(last is not None and last != bit)
                val = nexts.get(bit,(math.inf,-math.inf))
                nexts[bit]=(min(val[0],lo+incr),max(val[1],hi+incr))
        states=nexts
    return [min(p[0] for p in states.values()),max(p[1] for p in states.values())]


def observed_adjacent_score(s):
    return sum(a==b for a,b in zip(s,s[1:]) if a != "?" and b != "?")


def permutation_null(s: str, *, n=12000, seed=20261012, frames=False):
    """Shuffle ONLY observed labels. Preserve missing mask and either global
    zone counts or observed counts in each consecutive nine-cell frame.
    Avoid model-predicted physical completions entirely.
    """
    rng = random.Random(seed)
    intervals = [(i,min(i+9,len(s))) for i in range(0,len(s),9)] if frames else [(0,len(s))]
    arr = list(s)
    groups = [[i for i in range(a,b) if s[i]!="?"] for a,b in intervals]
    observed = observed_adjacent_score(s)
    scores=[]
    for _ in range(n):
        t=arr.copy()
        for group in groups:
            marks=[s[i] for i in group]
            rng.shuffle(marks)
            for i,c in zip(group,marks): t[i]=c
        scores.append(observed_adjacent_score(t))
    mean=sum(scores)/n
    var=sum((v-mean)**2 for v in scores)/n
    return {"observed_matching_adjacent":observed,"replicates":n,"mean":round(mean,6),
            "sd":round(math.sqrt(var),6),"min":min(scores),"max":max(scores),
            "one_sided_ge":round((1+sum(x>=observed for x in scores))/(n+1),6),
            "one_sided_le":round((1+sum(x<=observed for x in scores))/(n+1),6),
            "method":"nine-site observed-count shuffled" if frames else "zone observed-count shuffled",
            "seed":seed}


def parser_null(s: str, *, n=1000, seed=411, frames=False):
    """Permutation reference for the *best* grammar acceptance rate over
    both polarity choices and the full fixed grammar portfolio. This adjusts
    the search over codebooks, preventing a best-of-six illusory discovery.
    """
    rng = random.Random(seed)
    groups = [[i for i in range(a, min(a+9, len(s))) if s[i] != "?"]
              for a in range(0,len(s),9)] if frames else [[i for i,c in enumerate(s) if c != "?"]]
    def score(t):
        pairs = (bit_string(t,tok[0],tok[1]) for tok in ("01", "10"))
        # t already encoded as 0,1,? -- swapping raw binary polarity.
        return max(parse_program(q, cb)["program_completions"]
                   for q in pairs for cb in CODEBOOKS.values())
    obs = score(s)
    scores=[]
    for _ in range(n):
        v=list(s)
        for indices in groups:
            marks=[s[i] for i in indices]
            rng.shuffle(marks)
            for j,bit in zip(indices, marks):v[j]=bit
        scores.append(score("".join(v)))
    scores.sort()
    return {"best_accepted_completions":obs,"replicates":n,
            "null_median":scores[n//2],"null_q95":scores[min(n-1,int(n*.95))],
            "max_family_ge_probability":round((1+sum(x>=obs for x in scores))/(n+1),6),
            "seed":seed,"frames":frames,
            "note":"retrospective best-of-models control; not a prospective p-value"}


def delimiter_bounds(s, delimiter: str):
    # Counts of exact delimiter occurrences, including overlapping occurrences.
    possible, certain=[],[]
    for i in range(len(s)-len(delimiter)+1):
        part=s[i:i+len(delimiter)]
        if matches(part,delimiter):
            possible.append(i+1)
            if "?" not in part:
                certain.append(i+1)
    return {"delimiter":delimiter,"certain_starts":certain,"possible_count":len(possible),
            "certain_count":len(certain),"uncertain_count":len(possible)-len(certain)}


def slash_as_single_bit(physical: str, slash_bit: str = "1"):
    """Cross-zone collapse: / vs (dash OR dot). Intentional invented rival.

    The two physical alphabets remain recorded distinctly in the source; this
    binary view is a possible interpretation, NOT a correction to the corpus.
    """
    other = "0" if slash_bit == "1" else "1"
    return "".join("?" if c == "?" else slash_bit if c == "/" else other
                   for c in physical)


def traversal(s: str, ordering: str):
    """Simple physically/canonically motivated H108 traversals. Index choices
    are frozen before looking at parser output. Reversals are separate trials.
    """
    if ordering == "serial":
        return s
    if ordering == "reverse_serial":
        return s[::-1]
    order = "ABCDEFGHI" if "class_A_I" in ordering else "IABCDEFGH"
    if ordering not in ("class_A_I","reverse_class_A_I","picture_IAB_CDE_FGH","reverse_picture_IAB_CDE_FGH"):
        raise ValueError(ordering)
    part = "".join(s[ord(c)-ord("A")::9] for c in order)
    return part[::-1] if ordering.startswith("reverse_") else part


FULL_TRAVERSALS=("serial","reverse_serial","class_A_I","reverse_class_A_I",
                 "picture_IAB_CDE_FGH","reverse_picture_IAB_CDE_FGH")


def cross_zone_null(s: str, *, n=200, seed=20261012, frame9=False):
    """Multiple-comparison control for best of 6 traversals, 2 polarities,
    and 6 full-stream program languages, preserving original physical zones.
    """
    rng=random.Random(seed)
    slices=[(start,min(start+9,end)) for a,end in ((0,81),(81,108))
            for start in range(a,end,9)] if frame9 else [(0,81),(81,108)]
    groups=[[i for i in range(a,b) if s[i]!="?"] for a,b in slices]
    def best(t):
        return max(parse_program(traversal(slash_as_single_bit(t,polarity),view),cb)["program_completions"]
                   for view in FULL_TRAVERSALS for polarity in ("1","0") for cb in CODEBOOKS.values())
    observed=best(s)
    vals=[]
    for _ in range(n):
        chars=list(s)
        for indices in groups:
            labels=[s[i] for i in indices]
            rng.shuffle(labels)
            for i,label in zip(indices,labels):chars[i]=label
        vals.append(best("".join(chars)))
    vals.sort()
    return {"observed_best":observed,"shuffles":n,"null_median":vals[n//2],
            "null_q95":vals[min(n-1,int(n*.95))],
            "fraction_ge_best":f"{1+sum(v>=observed for v in vals)}/{n+1}",
            "seed":seed,"frame9":frame9,"search_size":len(FULL_TRAVERSALS)*2*len(CODEBOOKS),
            "note":"post-selection ensemble maximum; cross-zone slash-vs-nonslash mapping assumed"}


def cross_zone_audit(s: str, *, n=200):
    out={"interpretation":"slash vs dash-or-dot collapses distinct 81/27 alphabets; speculative",
         "traversals":{},"null_controls":{}}
    for view in FULL_TRAVERSALS:
        partial=traversal(s,view)
        out["traversals"][view]={}
        for slash in ("1","0"):
            bits=slash_as_single_bit(partial,slash)
            out["traversals"][view][f"slash={slash}"]={
                "grammar":{k:{"program_completions":v["program_completions"],
                              "with_control_completions":v["with_control_completions"]}
                           for k,book in CODEBOOKS.items() if (v:=parse_program(bits,book))},
                "observed_adjacent_pairs":contiguous_observation(bits)["known_adjacent_pairs"],
                "matching_adjacent_pairs":contiguous_observation(bits)["matching_pairs"]}
    out["null_controls"]["original_zone_shuffles"] = cross_zone_null(s,n=n,seed=20261020)
    out["null_controls"]["original_nine_site_frame_shuffles"] = cross_zone_null(s,n=n,seed=20261021,frame9=True)
    return out


def one_hot_tail_audit(tail: str):
    """Independent class-local 9+3 instruction-header census, with exact nulls.

    Original raw H108 order: each class A..I occupies one site in each
    nine-wide row. The last three occurrences of each class form its opcode.
    This is a competing hypothetical grammar, not a U2 machine completion.
    """
    assert len(tail) == 27 and all(x in "/.?" for x in tail)
    def options(word, mark):
        other = "." if mark == "/" else "/"
        return [j for j in range(3) if all(c == "?" or c == (mark if i == j else other)
                                         for i,c in enumerate(word))]
    def class_count(word, mark):
        out=1
        for i in range(9):
            out *= len(options("".join(word[i+9*j] for j in range(3)),mark))
        return out
    classes={}
    for i,name in enumerate("ABCDEFGHI"):
        segment="".join(tail[i+9*j] for j in range(3))
        classes[name]={"physical":segment,"residues":[82+i,91+i,100+i],
                       "slash_op_positions":options(segment,"/"),"dot_op_positions":options(segment,".")}
    known=[i for i,c in enumerate(tail) if c!="?"]
    slash_total=sum(tail[i]=="/" for i in known)
    frame_groups=[[i for i in known if 9*j<=i<9*(j+1)] for j in range(3)]
    frame_slashes=[sum(tail[i]=="/" for i in grp) for grp in frame_groups]
    counts={}
    for model in ("global_observed_counts","nine_frame_observed_counts"):
        if model=="global_observed_counts":
            selections=(set(c) for c in itertools.combinations(known,slash_total))
        else:
            combos=(itertools.combinations(group,k) for group,k in zip(frame_groups,frame_slashes))
            selections=(set().union(*groups) for groups in itertools.product(*combos))
        slash_survive=dot_survive=total=0
        slash_counts=Counter()
        for choice in selections:
            model_word="".join("?" if i not in known else "/" if i in choice else "."
                               for i in range(27))
            sc=class_count(model_word,"/"); dc=class_count(model_word,".")
            slash_survive += int(sc>0); dot_survive += int(dc>0)
            slash_counts[sc] += 1
            total += 1
        counts[model]={"support":total,"compatible_one_slash":slash_survive,
                       "compatible_one_dot":dot_survive,
                       "one_slash_fraction":f"{slash_survive}/{total}",
                       "one_dot_fraction":f"{dot_survive}/{total}",
                       "one_slash_completion_counts":dict(sorted(slash_counts.items()))}
    return {"classes":classes,"one_slash_completions":class_count(tail,"/"),
            "one_dot_completions":class_count(tail,"."),
            "exact_observation_label_permutation_nulls":counts,
            "note":"Compatibility only; 427 dot eliminates half the historically reported 36 one-slash completions."}


def analyze(s, nperm=12000, nparser=500, ncross=200):
    assert len(s)==108
    out={"status":"DISCOVER/DEVELOP only; no identified decoder", "corpus":{"records":None,"distinct_observed":len(s)-s.count("?"),"unknown":s.count("?"),"h108_length":108},"zones":{}}
    for start,end,label,symbols in ZONES:
        zone=s[start-1:end]
        assert all(x in symbols+"?" for x in zone)
        z={"residues":[start,end],"symbols":symbols,"partial":zone,"observed":len(zone)-zone.count("?"),"unknown":zone.count("?"),
           "observed_counts":dict(Counter(c for c in zone if c!="?")),"contiguous":contiguous_observation(zone),
           "fixed_groups":fixed_groups(zone),"delimiters":{},"bit_mappings":{},
           "nulls":{"global":permutation_null(zone,n=nperm,seed=20261012+start),
                    "frame9":permutation_null(zone,n=nperm,seed=20261112+start,frames=True)}}
        for a in symbols:
            for size in range(1,4):
                # Two distinct meanings: homogeneous delimiter and alternation.
                for delim in (a*size,):
                    z["delimiters"][delim]=delimiter_bounds(zone,delim)
        for mapping in (symbols, symbols[::-1]):
            bits=bit_string(zone,mapping[0],mapping[1]); key=mapping[0]+"=0,"+mapping[1]+"=1"
            z["bit_mappings"][key]={"transitions_min_max":exact_markov_transitions(bits),
                "exact_run_counts_min_max":{str(k):completed_runs(bits,k) for k in range(1,13)},
                "grammar":{g:parse_program(bits,book) for g,book in CODEBOOKS.items()}}
        z["nulls"]["parser_best_of_family_global"] = parser_null(bit_string(zone,symbols[0],symbols[1]),n=nparser,seed=20261212+start)
        z["nulls"]["parser_best_of_family_frame9"] = parser_null(bit_string(zone,symbols[0],symbols[1]),n=nparser,seed=20261312+start,frames=True)
        out["zones"][label]=z
    out["mixed_width_grouping_counts"]={str(n):mixed_width_partitions(n) for n in (12,27,81,108)}
    out["cross_zone_class_metadata"] = one_hot_tail_audit(s[81:])
    out["cross_zone_slash_binary"] = cross_zone_audit(s,n=ncross)
    return out


def test():
    assert traversal("ABCDEF","serial")=="ABCDEF"
    assert traversal("ABCDEF","reverse_serial")=="FEDCBA"
    assert slash_as_single_bit("-/./?", "1")=="0101?"
    assert mixed_width_partitions(12)["ordered_partitions_total"]==1
    assert mixed_width_partitions(27)["ordered_partitions_total"]==36
    assert mixed_width_partitions(81)["ordered_partitions_total"]==447702
    assert mixed_width_partitions(108)["ordered_partitions_total"]==53501860
    assert all(is_prefix_free(x) for x in CODEBOOKS.values())
    assert not is_prefix_free({"0":None,"01":None})
    assert matches("?0?","101") and not matches("00","01")
    assert completed_runs("00011",3)==[1,1]
    assert completed_runs("0?1",1)==[1,1]
    assert exact_markov_transitions("01?")==[1,2]
    assert parse_program("00000",CODEBOOKS["two_bit_backward"])["program_completions"]==1 # 00 + three zeros
    assert parse_program("100",CODEBOOKS["two_bit_backward"])["program_completions"]==0 # cannot repeat before emit
    assert parse_program("0000010",CODEBOOKS["two_bit_backward"])["program_completions"]==1 # emit then repeat
    assert parse_program("???",CODEBOOKS["prefix_backward"])["program_completions"]==0
    assert parse_program("???",CODEBOOKS["prefix_forward"])["program_completions"]==0
    # Against exhaustive independent non-DP interpreter on all short strings.
    from itertools import product
    for cb in CODEBOOKS.values():
        for length in range(9):
            for combo in product("01", repeat=length):
                bits = "".join(combo)
                accepted = execute_complete_program(bits,cb) is not None
                assert parse_program(bits,cb)["program_completions"] == int(accepted), (bits,cb)
    for length in range(1,8):
        for combo in product("01?", repeat=length):
            partial = "".join(combo)
            if partial.count("?") > 4: continue
            compatible = ["".join(v) for v in product("01",repeat=length) if matches(partial,"".join(v))]
            brute = sum(execute_complete_program(v,CODEBOOKS["two_bit_backward"]) is not None for v in compatible)
            assert brute == parse_program(partial,CODEBOOKS["two_bit_backward"])["program_completions"]
    for length in range(1,7):
        for combo in product("01?",repeat=length):
            partial="".join(combo)
            if partial.count("?")>4: continue
            words=["".join(v) for v in product("01",repeat=length) if matches(partial,"".join(v))]
            for k in range(1,4):
                counts=[]
                for word in words:
                    stretches=[]; run=1
                    for i in range(1,len(word)):
                        if word[i]==word[i-1]:run+=1
                        else:stretches.append(run);run=1
                    stretches.append(run)
                    counts.append(stretches.count(k))
                assert completed_runs(partial,k)==[min(counts),max(counts)]
    # For any fully observed word, deterministic prefix grammar accepts <=1 parse.
    for cb in CODEBOOKS.values():
        for i in range(256):
            p=format(i,"08b")
            assert parse_program(p,cb)["program_completions"] in (0,1)
    # A completed input must never have ambiguous parse, even with both side operations.
    assert parse_program("?0???",CODEBOOKS["two_bit_backward"])["program_completions"]<=16
    assert one_hot_tail_audit("?"*27)["one_slash_completions"] == 3**9
    assert one_hot_tail_audit("."*27)["one_slash_completions"] == 0
    assert parse_program("0000011",CODEBOOKS["two_bit_terminated"])["program_completions"] == 1
    assert parse_program("00000",CODEBOOKS["two_bit_terminated"])["program_completions"] == 0


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--observations",type=Path,default=Path("data/observations.csv"))
    ap.add_argument("--output",type=Path,default=Path("data/conjecture-lab-variable-length-grammar-2026-10-12.json"))
    ap.add_argument("--replicates",type=int,default=12000)
    ap.add_argument("--parser-null-replicates",type=int,default=500)
    ap.add_argument("--cross-null-replicates",type=int,default=200)
    ap.add_argument("--test",action="store_true")
    args=ap.parse_args()
    test()
    if args.test:
        print("parser and run-DP invariants passed")
        return
    s,n=load_observations(args.observations)
    report=analyze(s,nperm=args.replicates,nparser=args.parser_null_replicates,ncross=args.cross_null_replicates)
    report["corpus"]["records"]=n
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    for zone,z in report["zones"].items():
        print(zone, "observed", z["observed"],"unknown",z["unknown"],"pairs",z["contiguous"]["known_adjacent_pairs"], "matches",z["contiguous"]["matching_pairs"])
        print("  shuffle p>=",z["nulls"]["global"]["one_sided_ge"],"frame9",z["nulls"]["frame9"]["one_sided_ge"])
        print("  parser best-family nulls:",z["nulls"]["parser_best_of_family_global"],z["nulls"]["parser_best_of_family_frame9"])
        for mapping,v in z["bit_mappings"].items():
            print(" ",mapping,"transition range",v["transitions_min_max"])
            for g,p in v["grammar"].items():
                print("    ",g,"accepted",p["program_completions"],"of",p["possible_completions"])
    print("tail class one-hot",report["cross_zone_class_metadata"]["one_slash_completions"],
          "exact null",report["cross_zone_class_metadata"]["exact_observation_label_permutation_nulls"])
    print("mixed-width 3/5 grouping counts",{n:d["ordered_partitions_total"] for n,d in report["mixed_width_grouping_counts"].items()})
    print("cross-zone controls",report["cross_zone_slash_binary"]["null_controls"])
    print("wrote",args.output)

if __name__=="__main__":
    main()