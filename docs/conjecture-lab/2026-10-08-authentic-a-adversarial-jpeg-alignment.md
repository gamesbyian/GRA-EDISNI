# CL-10: does authentic A increase the *stable* recovered 534brn evidence?

_8 October 2026. Source-first adversarial validation of a damaged-image alignment, not foreground-code decoding._

## Answer

**No.** [CL-09](2026-10-08-terminal41-unarchived-route-recovery.md) finally recovered the **byte-identical original 12,140-byte A capture** of the unresolved Terminal41 `534brn` page. The older connector-transformed version had 12,150 bytes. Under a single frozen alignment heuristic, this correction increased the number of candidates filling gaps in B from **238 to 245**. That raised the obvious question: does it also increase the number of recoveries robust to equally plausible edit alignments?

We reran the exact previous five-way experiment, using **authentic original A**, unchanged byte-authenticated B/P, and the same tokenizer/anchor rules/edit costs from `scripts/audit_534brn_alignment_sensitivity.py` without changing **any** candidate or scoring parameters. Outcomes:

| Alignment variant | Old rendition A: candidate fills | True original A: candidate fills | True A: conflicts |
|---|---:|---:|---:|
| 12-byte known anchors; diagonal ties | 238 | **245** | 10 |
| 12-byte anchors; upward ties | 265 | **277** | 10 |
| 12-byte anchors; leftward ties | 265 | **273** | 30 |
| 10-byte anchors; diagonal ties | 238 | **245** | 10 |
| 14-byte anchors; diagonal ties | 238 | **245** | 10 |

The true-A baseline has **245** proposed fills. Only **18 of those 245** have the **same candidate position and value across all five** tested alternatives:

```
8676=36  8677=20  8686=37  8688=11  8692=46  8694=50
9278=0b  9279=18  9282=63  9283=3f  9287=37  9288=44
9292=65  9296=56  9297=38  9300=55  9302=3c  9764=65
```

There are **227 variable baseline values**. Eight fail merely by choosing upward instead of diagonal tie-breaking; 227 fail under leftward tie-breaking. The 10-/14-byte anchor tweaks alone do not alter the selected diagonal result. The older rendition also had exactly **18 consensus fills** under the same five variants. Authentic bytes changed candidate identities and counts, **not the consensus cardinality**.

None of this proves the 18 are uniquely compelled original JPEG bytes. This is consensus across **five chosen minimum-cost edit paths**, not a mathematical enumeration of all optimal paths or an independent positional proof. The original high-byte/Unicode replacement loss in B and P remains, and no valid JPEG has been reconstructed. We do **not** infer a 128×128 image or nine-sticker-to-entropy repair algorithm from this count.

## Reproducibility

The original GHA run [CL-10 source evidence](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/37866759723) ran the exact Python source against the four source-authenticated bytes and recorded the complete alternative alignment maps and changed positions. The repository retains a compact [18-value and five-path result fixture](../../data/534brn-true-a-adversarial-alignment-2026-10-08.json) and [executable adversarial replay](../../scripts/audit_534brn_true_a_alignment_sensitivity.py). The original source A's SHA-1 `ce55c03ee972954f6e80f55a1a279bb85024f99b` is verified as a Git blob.

```bash
python scripts/audit_534brn_true_a_alignment_sensitivity.py
python scripts/audit_534brn_true_a_alignment_sensitivity.py --output-json /tmp/true-a-5-paths.json
```

The second command re-emits the entire per-variant list of shifted candidate offsets, whereas the compact fixture preserves its evidence-bearing count and 18-candidate consensus values. A different future source capture could supply new independent constraints and might change the result.

## Decision consequence

The root cause of uncertainty is **ambiguous positional alignment between streams with extensive byte information loss**, not merely the original A's ten-byte transcoding problem. Further brute-force JPEG pixel guesses or tie-breaking changes are unlikely to create independent knowledge.

The research frontier should be **raw contemporaneous backups** (most conspicuously the photographed but unarchived `saf_dat_col_BACKUP.html`) or truly independent source fields, rather than promoting one particular heuristic completion to fact. If new sources appear, their byte identities and transformations must be authenticated *first*, then evaluated on a fixed, frozen alignment protocol.

**CL-10 status:** Source-corrected heuristic recovery **245**, five-path robust consensus **18**, guaranteed uniquely decoded original JPEG bytes **not established**, CE foreground decoder **not established**.
