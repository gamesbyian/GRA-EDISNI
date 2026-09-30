#!/usr/bin/env python3
"""Experiment 336: expand frozen row-selector discriminating residues to physical serials."""

from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FROZEN={84:".",102:"/"}

def load_observed_serials(path:Path)->set[int]:
    with path.open(newline="",encoding="utf-8") as fh:
        return {int(row["serial"]) for row in csv.DictReader(fh)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--observations",default="data/observations.csv")
    ap.add_argument("--max-serial",type=int,default=600)
    args=ap.parse_args()
    observed=load_observed_serials(Path(args.observations))
    rows=[]
    for residue,symbol in FROZEN.items():
        serial=residue
        while serial<=args.max_serial:
            rows.append({
              "serial":serial,"residue":residue,"background":"C",
              "frozen_row_selector_symbol":symbol,
              "already_observed_exact_serial":serial in observed,
            })
            serial+=108
    rows.sort(key=lambda x:x["serial"])
    out={
      "max_serial":args.max_serial,
      "discriminating_residues":{"84":".","102":"/"},
      "physical_serial_count":len(rows),
      "unobserved_exact_serial_count":sum(not x["already_observed_exact_serial"] for x in rows),
      "serials":rows,
      "falsification_rule":"Any provenance-backed residue-84 slash or residue-102 dot falsifies the frozen Experiment-329 row-selector family.",
      "caution":"Agreement supports the frozen rival prospectively but does not by itself identify the incumbent hidden state because broader incumbent physical gauges also exist."
    }
    assert [x["serial"] for x in rows]==[84,102,192,210,300,318,408,426,516,534]
    assert out["unobserved_exact_serial_count"]==10
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
