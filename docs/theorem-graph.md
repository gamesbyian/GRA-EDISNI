# Mechanical theorem graph

_Status: Experiment 241, post-240 proof-pack pass._

This document separates supplied observations/grammars from derived consequences in the current closed-corpus machine. It is intentionally narrower than the historical Results document: the goal is to make circular support and redundant premises obvious.

## Node classes

- **O** — physical observation / carrier fact
- **G** — supplied local grammar or bounded model-class choice
- **T** — derived theorem / exact consequence
- **R** — observer/readout fact, not part of the transition generator
- **A** — descriptive algebraic characterization, not a physical mechanism
- **S** — semantic stopping statement

## Minimal transition chain

| ID | Class | Claim | Direct dependencies |
|---|---|---|---|
| O1 | O | Serial foreground period is 108 and background image class cycles A–I with period 9. | corpus |
| O2 | O | H108 address factorization is `r-1 = 27q + 9d + j`; residues 1–81 use slash/dash and 82–108 use slash/dot. | O1, corpus |
| G1 | G | Primary columns use POS3: ternary value is the position of the exceptional member in a three-cell rail. | O2 |
| G2 | G | Primary frame polarity follows the triangular staircase: minority symbol is dash iff `d<=q`. Raw data under G1 fixes 8/9 frame polarities; only `q=1,d=2` needs the global staircase completion. | O2, G1 |
| T1 | T | Under G1–G2, raw observations force 25/27 primary payload trits; the only unresolved trits are `x=(q0,d2,c1)∈{1,2}` and `y=(q2,d0,c1)∈{0,1,2}`. | O2, G1, G2 |
| T1a | T | All 18 outer primary trits are observation-forced and satisfy minority-row `!=d`; the old outer no-self rule is therefore derived rather than an additional premise. | T1 |
| T1b | T | The primary payload family reduces to `112 212 0x0 / 212 002 100 / 1y2 022 100`, with the route/cross normal form described in current-state. | T1, T1a |
| G3 | G | Q4 uses one shared-polarity POS3 orientation across all nine depth stacks. | O2 |
| T2a | T | Raw Q4 observations force the shared exceptional symbol to slash (36 compatible slash-exception completions, zero dot-exception completions), yielding exactly 36 selector completions. | O2, G3 |
| G5 | G | First recursive application substitutes selector depth into the primary address: `(q,d,j)->(q,S(j),j)`. | T1b, T2a |
| T3a | T | Cartesian product of the 6 raw-compatible primary payloads and 36 raw-compatible selectors gives 216 candidate machines; first-pass POS3 closure leaves 20. | T1b, T2a, G5 |
| G6 | G | The same selector is reused on the regenerated surfaces: `(q,S(j),j)->(S(j),S(j),j)`. | G5 |
| T2 | T | Second-pass POS3 closure reduces 20→14 and reconstructs the Q4 control family: C is a free {0,2} gauge and A/D/G cores are exactly `110/220/212`. | T3a, G6 |
| T3 | T | The 14 survivors have exactly three first-pass functional outputs; hidden-state dependence falls 14→3. | T2, G5 |
| T4 | T | The request/grant relation `00->1, 01->0, 10->2, 11->{0,2}`, equivalently eligibility `[X,NOR(X,Y),Y]`, emerges from surviving primary ports versus the three reconstructed control cores. | T2, T3 |
| T5 | T | `210` supplies route reindex `q=2-p`; Q3 completes to `102/012/120`. | T3, T4 |
| T6 | T | Every one of the 14 second-pass survivors canonicalizes to frame 9 / payload `100` / raw `---//////`; terminal `100` is not used as a selection filter. | T2, G6 |

Taking the two recursive operations G5–G6 as the operation grammar, the present transition-side supplied set is **O1–O2 + G1–G3 + G5–G6**. Experiment 246 materially weakens G2: eight of its nine frame polarities are directly forced by the corpus under POS3, leaving only one upper-triangle completion to the global staircase rule. Experiment 254 materially weakens G3: only shared Q4 POS3 polarity is supplied; the slash-exception orientation is forced by observations. Experiments 250–252 remove the former Q4 canonical-shell reconstruction premise from the minimal generation chain: the surviving Q4 scaffold/control family is recovered by closure from the 36 raw selector completions. The former outer no-self grammar is likewise theorem-level.

## State and storage chain

| ID | Class | Claim | Direct dependencies |
|---|---|---|---|
| T7 | T | Native state may be expressed as `(x,y,p,g)` with `x∈{1,2}`, `y∈{0,1,2}`, `g∈{0,2}` and the request/grant relation T4. | T4 |
| T8 | T | T7 admits exactly 14 physical states. | T7 |
| T9 | T | Equivalent Boolean normal form is `H=(X,Y,Z,G)` with one Horn clause `Y & Z -> X`. | T7, T8 |
| T10 | T | The 13 variable residues factor into X complement pair, y one-hot triple, G complement pair, and p one-hot/complement rails. | T7, generated masters |
| T11 | T | Every complete master has 95 invariant / 13 variable residues and census 54/36/18. | T7, T1, T2 |
| T12 | T | The latent register has weight 6 and minimum Hamming distance 2. | T10 |

The Boolean near-cube is a compression of the native relation, not a premise required to generate the machine.


## Robustness boundary beyond the exact state family

Experiment 255 tests a broader primary grammar in which each primary column may contain zero or one minority-symbol pulse. Raw observations allow 1,536 such primary completions. With the 36 Q4 selectors, recursive POS3 closure leaves 832 states. Every survivor still terminates at `100`, but only 14 have one occupied minority pulse in all 27 columns.

Therefore G1 has two distinct roles:

- **exact-state role:** exact POS3 is needed to select the canonical 14-state physical family;
- **endpoint role:** exact POS3 is not needed for terminal `100` inside the tested zero-or-one-pulse parent grammar.

This distinction prevents overclaiming uniqueness while strengthening the terminal's robustness.

## Observer branch

| ID | Class | Claim | Direct dependencies |
|---|---|---|---|
| R1 | R | Frozen same-quarter and Q4-target queries form an 18-bit observer bus. | preregistered pointer geometry |
| R2 | R | The bus is injective over the 14 physical states. | R1, T8 |
| R3 | R | Four nonlinear postprocessed bits recover `XYZG`; raw-query minima are 3/4/5 for the documented quotients. | R2 |

R1–R3 do not generate T1–T6. They may discriminate otherwise surviving model forks, but cannot be used as if they were transition evidence unless that use is declared explicitly.

## Algebra branch

| ID | Class | Claim | Direct dependencies |
|---|---|---|---|
| A1 | A | Route maps `120` and `102` generate `S3`. | T5 |
| A2 | A | Adding terminal `100` generates the full 27-map transformation monoid `T3`. | A1, T6 |
| A3 | A | Ordinary map composition does not reproduce the physical selector dynamics. | A1, A2, G5, G6 |

A1–A2 describe closure properties. A3 prevents them from being silently promoted into a physical mechanism.

## Semantic stop

| ID | Class | Claim | Direct dependencies |
|---|---|---|---|
| S1 | S | Established INSIDE ARG consumer families do not supply a completion-invariant downstream consumer for `100 / ---//////`. | Experiment 240, T6 |
| S2 | S | The mechanically justified endpoint is therefore T6 unless independent evidence supplies a new consumer. | S1 |

## Immediate proof obligations exposed by this graph

1. **G1/G2:** Experiment 255 shows zero-or-one-pulse weakening does not recover the exact 14-state family, although terminal `100` survives; broader primary grammars should distinguish exact-family uniqueness from endpoint robustness.
2. **G3:** Experiment 254 reduces the supplied commitment to shared-polarity Q4 POS3; test grammars that weaken shared orientation itself without exploding the closure family.
3. **G5/G6:** extend Experiment 253 beyond shell-preserving coordinate permutations. Within that raw-space family the canonical recursion is unique up to external-q relabeling under maximal raw-state retention.
4. **T7–T11:** the lower-level constraint/enumeration target is now satisfied by Experiments 250–251; use it as the preferred independence oracle for future state-family changes.
5. **R1:** keep observer evidence quarantined when auditing transition uniqueness.

Experiment 241 created the graph; Experiments 246 and 250–253 have since reduced it. The current raw-constraint chain no longer needs outer no-self or a separately supplied Q4 scaffold/control reconstruction, and the state-language conversions are downstream descriptions of the 14-state closure family.
