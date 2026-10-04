#!/usr/bin/env python3
"""Experiment 365: layered H108 completion-universe generator and query surface.

The broad enumerable layer deliberately stops before the incumbent recursion:
  U0  raw 42-bit foreground assignments (symbolic: 2^42)
  U1  common 3/6 or 4/5 primary census x one-slash-per-class Q4 (factored)
  U2  3/6 one-per-physical-column primary x one-slash-per-class Q4 (324 masters)
  U3  established polarity + exact POS3 (108 raw machines)
  U4  first recursive closure (12)
  U5  second recursive closure (10 canonical masters)

The known physical-representation gauges are reported separately because the
primary transition-invisible gauges need not remain inside U2's preferred
one-per-column representation.
"""
from __future__ import annotations
import argparse, csv, itertools, json, math
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OBS=ROOT/"data"/"observations.csv"
OUT=ROOT/"data"/"experiment-365-completion-universe.json"
U2=ROOT/"data"/"completion-universe-u2-324.csv"
SERIAL="ABCDEFGHI"
LAYOUT=("IAB","CDE","FGH")
POS={ch:(r,c) for r,row in enumerate(LAYOUT) for c,ch in enumerate(row)}

def product_dict(options):
    return itertools.product(*options)

def load_observations():
    out={}
    with OBS.open(newline="",encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            r=int(row["residue"]); s=row["symbol"]
            if r in out and out[r]!=s: raise AssertionError(f"conflict at residue {r}")
            out[r]=s
    assert len(out)==66
    return out

def primary_frame_options(obs,frame):
    out=set()
    for minority in ("/","-"):
        majority="-" if minority=="/" else "/"
        for selected_rows in itertools.product(range(3),repeat=3):
            chars=[]
            for j,letter in enumerate(SERIAL):
                row,col=POS[letter]
                chars.append(minority if row==selected_rows[col] else majority)
            text="".join(chars)
            if all(obs.get(frame*9+j+1,text[j])==text[j] for j in range(9)):
                out.add(text)
    return tuple(sorted(out))

def tail_options(obs):
    result=[]
    for j in range(9):
        allowed=[]
        for selected_depth in range(3):
            if all(
                obs.get(82+d*9+j, "/" if d==selected_depth else ".")
                == ("/" if d==selected_depth else ".")
                for d in range(3)
            ):
                allowed.append(selected_depth)
        result.append(tuple(allowed))
    return tuple(result)

def master_from(primary,selector):
    tail="".join("/" if selector[j]==d else "." for d in range(3) for j in range(9))
    return primary+tail

def unknown_residues(obs):
    return tuple(r for r in range(1,109) if r not in obs)

def encode_unknown43(master,unknown):
    value=0
    for i,r in enumerate(unknown):
        if master[r-1]=="/": value|=1<<i
    return f"{value:011x}"

def decode_unknown43(code,obs,unknown):
    value=int(code,16); chars=["?"]*108
    for r,s in obs.items(): chars[r-1]=s
    for i,r in enumerate(unknown):
        if value&(1<<i): chars[r-1]="/"
        else: chars[r-1]="-" if r<=81 else "."
    assert "?" not in chars
    return "".join(chars)

def census_primary_count(obs,w):
    counts=[]
    for frame in range(9):
        cells=[obs.get(frame*9+j+1,"?") for j in range(9)]
        slash=cells.count("/"); unknown=cells.count("?"); total=0
        for slash_total in {w,9-w}:
            need=slash_total-slash
            if 0<=need<=unknown: total+=math.comb(unknown,need)
        counts.append(total)
    return counts,math.prod(counts)

def build():
    obs=load_observations(); unknown=unknown_residues(obs)
    assert len(unknown)==42
    frame_opts=tuple(primary_frame_options(obs,f) for f in range(9))
    assert tuple(map(len,frame_opts))==(1,1,2,1,1,3,3,1,1)
    primaries=tuple("".join(parts) for parts in itertools.product(*frame_opts))
    assert len(primaries)==18
    tails=tail_options(obs)
    assert tuple(map(len,tails))==(3,1,3,1,1,1,2,1,1)
    selectors=tuple(itertools.product(*tails))
    assert len(selectors)==18

    masters=[]
    for pi,primary in enumerate(primaries):
        for si,selector in enumerate(selectors):
            master=master_from(primary,selector)
            assert all(master[r-1]==s for r,s in obs.items())
            code=encode_unknown43(master,unknown)
            assert decode_unknown43(code,obs,unknown)==master
            masters.append((pi,si,code,master))
    assert len(masters)==324
    assert len({m[2] for m in masters})==324

    rows=[]
    for r in unknown:
        c=Counter(master[r-1] for *_prefix,master in masters)
        H=-sum((n/324)*math.log2(n/324) for n in c.values())
        rows.append({
            "residue":r,
            "background":SERIAL[(r-1)%9],
            "candidate_counts":dict(c),
            "entropy_bits":H,
            "serials_1_600":list(range(r,601,108)),
        })
    rows.sort(key=lambda x:(-x["entropy_bits"],x["residue"]))

    def distinct_signatures(residues):
        return len({
            tuple(master[r-1] for r in residues)
            for *_prefix, master in masters
        })

    primary_discriminator=(22,49,50,55,58)
    tail_discriminator=(82,84,88,91,93)
    assert distinct_signatures(primary_discriminator)==18
    assert distinct_signatures(tail_discriminator)==18
    assert distinct_signatures(primary_discriminator+tail_discriminator)==324

    c3,n3=census_primary_count(obs,3); c4,n4=census_primary_count(obs,4)
    assert n3==12960 and n4==18000
    result={
        "experiment":365,
        "unknown_residue_count":42,
        "unknown_residues":list(unknown),
        "universes":{
            "U0_raw_binary":{"count":2**42,"materialization":"symbolic only"},
            "U1_common_census_plus_one_slash_tail":{
                "primary_3_6_completions":n3,
                "primary_4_5_completions":n4,
                "tail_one_slash_completions":18,
                "count":(n3+n4)*18,
                "materialization":"factored",
            },
            "U2_one_per_column_3_6_plus_one_slash_tail":{
                "primary_completion_count":18,
                "primary_frame_option_counts":list(map(len,frame_opts)),
                "tail_completion_count":18,
                "tail_class_option_counts":list(map(len,tails)),
                "count":324,
                "materialization":"complete 43-bit enumeration",
            },
            "U3_established_polarity_exact_pos3":{"count":108},
            "U4_first_recursive_closure":{"count":12},
            "U5_second_recursive_closure_canonical":{"count":10},
            "P_exact_physical_representation_expansion":{
                "canonical_states":10,
                "primary_gauge_combinations":4,
                "q4_A_C_gauge_combinations":4,
                "count":160,
                "nesting_note":"representation expansion around U5; not constrained to remain inside U2 geometry",
            },
        },
        "u2_residue_catalog":rows,
        "highest_information_u2_residues":[x["residue"] for x in rows if abs(x["entropy_bits"]-1)<1e-12],
        "u2_minimum_complete_discriminator":{
            "lower_bound_bits":10,
            "proof":"U2 factorizes into 18 primary x 18 tail; binary observations require at least 5+5 bits",
            "primary_residues":list(primary_discriminator),
            "tail_residues":list(tail_discriminator),
            "all_residues":list(primary_discriminator+tail_discriminator),
            "distinguished_primary_completions":18,
            "distinguished_tail_completions":18,
            "distinguished_complete_masters":324,
        },
        "guardrail":"candidate frequencies are combinatorial multiplicities, not calibrated probabilities",
    }
    return result,masters,unknown

def write():
    result,masters,unknown=build()
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    with U2.open("w",newline="",encoding="utf-8") as fh:
        w=csv.writer(fh); w.writerow(("id","primary_index","selector_index","unknown43_hex"))
        for i,(pi,si,code,_master) in enumerate(masters): w.writerow((i,pi,si,code))
    print(json.dumps(result,indent=2))

def query(residue):
    result,masters,_unknown=build()
    row=next(x for x in result["u2_residue_catalog"] if x["residue"]==residue)
    print(json.dumps(row,indent=2))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--query-residue",type=int)
    p.add_argument("--write",action="store_true")
    a=p.parse_args()
    if a.query_residue is not None: query(a.query_residue)
    else: write()

if __name__=="__main__": main()
