#!/usr/bin/env python3
"""Experiment 396: bounded boundary/check-bit registration audit.

Tests whether fixed-width edge signatures of the native 12-cell A-I class words
behave like useful ordering/check-bit metadata, analogous only at the operation
class level to the solved PC printer side marks.
"""

from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path

from build_completion_universe import build
from audit_completion_universe_layers import machine_layers
from audit_534brn_universe_survival import first_words

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-396-boundary-checkbit-audit.json"
SERIAL="ABCDEFGHI"
AI_ORDER=tuple(range(9))
PHYSICAL_ORDER=(8,0,1,2,3,4,5,6,7)  # I,A,B,C,D,E,F,G,H

def class_rows(master):
    return tuple(
        "".join(master[j+9*k] for k in range(12))
        for j in range(9)
    )

def signature(row,width):
    return row[:width]+row[12-width:]

def hamming(a,b):
    return sum(x!=y for x,y in zip(a,b))

def path_cost(sigs,order):
    return sum(hamming(sigs[order[i]],sigs[order[i+1]]) for i in range(8))

def minimum_path_cost(sigs):
    n=9
    inf=10**9
    dp=[[inf]*n for _ in range(1<<n)]
    for j in range(n):
        dp[1<<j][j]=0
    for mask in range(1,1<<n):
        for j in range(n):
            if not (mask & (1<<j)):
                continue
            prev=mask^(1<<j)
            if not prev:
                continue
            best=inf
            for k in range(n):
                if prev & (1<<k):
                    best=min(best,dp[prev][k]+hamming(sigs[k],sigs[j]))
            dp[mask][j]=best
    return min(dp[-1])

def summarize(masters,width):
    distinct_hist={}
    ai_gaps=[]
    physical_gaps=[]
    ai_opt=0
    physical_opt=0

    for master in masters:
        sigs=tuple(signature(row,width) for row in class_rows(master))
        d=len(set(sigs))
        distinct_hist[d]=distinct_hist.get(d,0)+1

        minimum=minimum_path_cost(sigs)
        ai=path_cost(sigs,AI_ORDER)
        physical=path_cost(sigs,PHYSICAL_ORDER)
        ai_gaps.append(ai-minimum)
        physical_gaps.append(physical-minimum)
        ai_opt += ai==minimum
        physical_opt += physical==minimum

    def stats(vals):
        return {
            "min":min(vals),
            "max":max(vals),
            "mean":sum(vals)/len(vals),
            "optimal_count":sum(v==0 for v in vals),
        }

    return {
        "distinct_signature_histogram":dict(sorted(distinct_hist.items())),
        "all_nine_rows_unique_count":distinct_hist.get(9,0),
        "A_to_I_excess_over_optimum":stats(ai_gaps),
        "physical_IAB_CDE_FGH_excess_over_optimum":stats(physical_gaps),
        "A_to_I_optimal_count":ai_opt,
        "physical_order_optimal_count":physical_opt,
    }

def main():
    _summary,u2_rows,_unknown=build()
    u2=[m for *_prefix,m in u2_rows]
    _u3,u4,_u5=machine_layers()
    e2=[m for m in u4 if first_words(m)==("112","012","120")]
    assert len(e2)==2

    result={
        "experiment":396,
        "operation_family":"fixed-width native edge signatures as possible row registration/check bits",
        "carrier":"nine 12-cell class words A-I",
        "orders_tested":{
            "serial":"A B C D E F G H I",
            "solved_physical":"I A B C D E F G H",
        },
        "widths":{},
    }

    for width in (1,2,3,4):
        result["widths"][str(width)]={
            "U2":summarize(u2,width),
            "U4":summarize(u4,width),
            "E2":summarize(e2,width),
        }

    # Stable negative controls from exact enumeration.
    assert result["widths"]["1"]["U2"]["all_nine_rows_unique_count"]==0
    assert result["widths"]["2"]["U2"]["all_nine_rows_unique_count"]==0
    assert result["widths"]["3"]["U2"]["all_nine_rows_unique_count"]==0
    assert result["widths"]["4"]["U2"]["all_nine_rows_unique_count"]==243
    assert result["widths"]["4"]["U4"]["all_nine_rows_unique_count"]==4

    for width in result["widths"].values():
        for ensemble in width.values():
            assert ensemble["A_to_I_optimal_count"]==0
            assert ensemble["physical_order_optimal_count"]==0

    result["conclusion"]=(
        "Fixed-width edge signatures do not behave like robust PC-style ordering metadata. "
        "Widths 1-3 never uniquely label all nine rows in U2; width 4 does so for only 243/648 "
        "U2 masters and 4/20 U4 masters. More importantly, neither natural A-I order nor solved "
        "physical IAB/CDE/FGH order is ever a minimum-Hamming boundary path at widths 1-4 in "
        "U2, U4, or the externally selected pair. Close this cheap boundary-continuity ordering "
        "lane unless a sticker-native artifact identifies a specific boundary subset or metric."
    )

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
