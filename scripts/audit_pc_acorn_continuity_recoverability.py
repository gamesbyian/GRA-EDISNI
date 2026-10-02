#!/usr/bin/env python3
"""Experiment 363: show that continuity maximization does not recover the PC acorn."""
from __future__ import annotations
import json, random, statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"data/printer-reference/pc-ps4-raw.txt"
SOLVED=ROOT/"data/printer-reference/pc-ps4-acorn-order.txt"
OUT=ROOT/"data/experiment-363-pc-acorn-continuity-recoverability.json"
SEED=363
RESTARTS=100

def lines(path):
    return [x.strip() for x in path.read_text(encoding="utf-8").splitlines()
            if x.strip() and not x.startswith("#")]

def pair(a,b):
    return sum(1 if x==y else -1 for x,y in zip(a,b))

def path_score(order,w):
    return sum(w[a][b] for a,b in zip(order,order[1:]))

def greedy_start(rng,w,n):
    unused=set(range(n))
    cur=rng.randrange(n)
    path=[cur]; unused.remove(cur)
    while unused:
        # Tiny seeded jitter gives deterministic tie-breaking without encoding raw order.
        nxt=max(unused,key=lambda j:(w[path[-1]][j],rng.random()))
        path.append(nxt); unused.remove(nxt)
    return path

def local_opt(path,w):
    n=len(path)
    path=list(path)
    best=path_score(path,w)
    while True:
        improved=False
        for i in range(n):
            for j in range(i+1,n):
                q=path[:]
                q[i],q[j]=q[j],q[i]
                s=path_score(q,w)
                if s>best:
                    path,best=q,s
                    improved=True
                    break
            if improved:
                break
        if improved:
            continue
        for i in range(n):
            for j in range(i+1,n):
                q=path[:i]+list(reversed(path[i:j+1]))+path[j+1:]
                s=path_score(q,w)
                if s>best:
                    path,best=q,s
                    improved=True
                    break
            if improved:
                break
        if not improved:
            return path,best

def edge_set(path):
    return {tuple(sorted((a,b))) for a,b in zip(path,path[1:])}

def main():
    raw=lines(RAW); solved=lines(SOLVED)
    assert len(raw)==len(solved)==32 and set(raw)==set(solved)
    index={row:i for i,row in enumerate(raw)}
    canonical=[index[row] for row in solved]
    n=len(raw)
    w=[[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            w[i][j]=w[j][i]=pair(raw[i],raw[j])
    canonical_score=path_score(canonical,w)
    assert canonical_score==176

    rng=random.Random(SEED)
    runs=[]
    for k in range(RESTARTS):
        p=greedy_start(rng,w,n)
        p,s=local_opt(p,w)
        runs.append((s,p))
    runs.sort(key=lambda x:x[0],reverse=True)
    best_score,best_path=runs[0]
    scores=[s for s,_ in runs]
    overlap=len(edge_set(best_path)&edge_set(canonical))

    result={
        "experiment":363,
        "seed":SEED,
        "restarts":RESTARTS,
        "canonical_score":canonical_score,
        "local_optimum_score_min":min(scores),
        "local_optimum_score_mean":statistics.mean(scores),
        "local_optimum_score_max":best_score,
        "best_path_raw_indices_1_based":[x+1 for x in best_path],
        "canonical_undirected_adjacencies":31,
        "best_path_shared_canonical_adjacencies":overlap,
        "interpretation":"Continuity is a positive diagnostic on the known acorn order but not an identifying reconstruction objective; simple blind optimization finds much higher-scoring wrong paths."
    }
    assert min(scores)==296
    assert statistics.mean(scores)==314.9
    assert best_score==328
    assert overlap==9
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
