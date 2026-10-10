#!/usr/bin/env python3
"""CX-E5: does a shared two-input Boolean rule govern G/H/I triple controls?

The speculative 4 / 9 / (9+3) grammar has three occurrences of each
G/H/I class per quarter: serial positions 7-9, 16-18, 25-27. Treat slash
as binary 1 and the other character as binary 0, including Q4 dots.
Enumerate ALL sixteen two-input truth tables, with existential missing
observations. Compare all C(9,3)=84 candidate class triples for hindsight
selection. The inferred rule is DEVELOP only; no physical marks filled.
"""
import argparse
import csv
import json
from itertools import combinations, product
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CLASSES="ABCDEFGHI"
SELECTED="GHI"


def load(path):
    obs={}
    with Path(path).open(newline="",encoding="utf8") as f:
        for row in csv.DictReader(f):
            n=int(row["residue"])
            s=row["symbol"].strip()
            assert 1<=n<=108 and s in "/-."
            assert row["image_class"].strip() in ("", CLASSES[(n-1)%9])
            assert n not in obs or obs[n]==s
            obs[n]=s
    return obs


def site(n, obs):
    mark=obs.get(n)
    return None if mark is None else int(mark=="/")


def triples(obs, classes=SELECTED):
    data=[]
    for q in range(4):
        for cl in classes:
            i=CLASSES.index(cl)+1
            ids=[q*27+i+j*9 for j in range(3)]
            symbols=[obs.get(n,"?") for n in ids]
            assert all((s in "/-" if q<3 else s in "/.") or s=="?"
                       for s in symbols)
            bits=[site(n,obs) for n in ids]
            data.append({"quarter":q+1,"class":cl,"residues":ids,
                         "observed_symbols":"".join(symbols),"known_bits":bits})
    return data


def output(table,a,b):
    return (table>>(2*a+b))&1


def compatible_completions(table,known):
    a,b,c=known
    return [(x,y,output(table,x,y)) for x,y in product(range(2),repeat=2)
            if (a is None or x==a) and (b is None or y==b)
            and (c is None or output(table,x,y)==c)]


def table_survivors(triple_records):
    return [table for table in range(16) if all(
        compatible_completions(table,row["known_bits"])
        for row in triple_records)]


def frame_family(obs, residue):
    """Explicitly separate the mature conditional rival from observations."""
    if residue>81:
        cls=(residue-82)%9
        ids=[82+cls,91+cls,100+cls]
        allowed=set()
        for chosen in range(3):
            arr=["/" if r==chosen else "." for r in range(3)]
            if all(obs.get(ids[j],v)==v for j,v in enumerate(arr)):
                allowed.add(arr[ids.index(residue)])
        return sorted(allowed)
    frame=(residue-1)//9
    loc=(residue-1)%9
    allowed=set()
    for minority in "/-":
        other="-" if minority=="/" else "/"
        for choices in product(range(3),repeat=3):
            cells=[other]*9
            for j,r in enumerate(choices):
                cells[3*r+j]=minority
            if all(obs.get(9*frame+j+1,v)==v for j,v in enumerate(cells)):
                allowed.add(cells[loc])
    return sorted(allowed)


def run(path):
    obs=load(path)
    ghi=triples(obs)
    survivor=table_survivors(ghi)
    control={}
    for chosen in combinations(CLASSES,3):
        name="".join(chosen)
        control[name]=table_survivors(triples(obs,name))
    assert SELECTED in control
    assert control[SELECTED]==survivor
    inferred=survivor[0] if len(survivor)==1 else None
    forecasts=[]
    if inferred is not None:
        for row in ghi:
            ways=compatible_completions(inferred,row["known_bits"])
            assert ways
            for j,residue in enumerate(row["residues"]):
                if row["known_bits"][j] is not None:
                    continue
                possible={way[j] for way in ways}
                if len(possible)!=1:
                    continue
                bit=next(iter(possible))
                mark="/" if bit else ("." if row["quarter"]==4 else "-")
                old=frame_family(obs,residue)
                forecasts.append({
                    "residue":residue,"class":row["class"],
                    "conditional_xor_forecast":mark,
                    "mature_conditional_frame_family":old,
                    "disagrees_with_frame_family":mark not in old
                })
    contradict=[]
    for row in triples(obs,CLASSES):
        if not compatible_completions(6,row["known_bits"]):
            contradict.append({
                "quarter":row["quarter"],"class":row["class"],
                "residues":row["residues"],
                "observed_symbols":row["observed_symbols"]
            })
    counts={}
    for scores in control.values():
        k=str(len(scores))
        counts[k]=counts.get(k,0)+1
    return {
        "status":"after-selection DEVELOP; not physical proof",
        "known_residues":len(obs),
        "selected_classes":SELECTED,
        "selected_n_triples":len(ghi),
        "actual_partial_triples":ghi,
        "truth_table_definition":"bit(2*a+b), indexed 00,01,10,11",
        "all_16_survivor_ids":survivor,
        "selected_truth_table_bits_00_01_10_11":[output(inferred,a,b)
                                             for a,b in product(range(2),repeat=2)]
                                             if inferred is not None else None,
        "XOR_truth_table_id":6,
        "selected_forecasts":sorted(forecasts,key=lambda x:x["residue"]),
        "all_classes_XOR_physical_contradictions":contradict,
        "all_84_three_class_subsets_survivor_count_distribution":counts,
        "unique_XOR_subsets":[name for name,s in control.items() if s==[6]],
        "unique_boolean_subsets":[name for name,s in control.items() if len(s)==1],
        "caution":"GHI was chosen via conjectural 4/9/(9+3) split; the Boolean function is logically identified only after granting this field definition. Other triplets were searched here as an explicit selection audit."
    }


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--observations",type=Path,default=ROOT/"data/observations.csv")
    args=parser.parse_args()
    print(json.dumps(run(args.observations),indent=2))
