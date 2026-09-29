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
| G2 | G | Primary local registration: the two outer minority rows at depth `d` are not equal to `d`. | O2, G1 |
| T1 | T | The primary payload family reduces to `112 212 0x0 / 212 002 100 / 1y2 022 100`, with the route/cross normal form described in current-state. | O2, G1, G2 |
| G3 | G | Q4 is a depth-indexed POS3 selector encoded by one slash per depth stack. | O2 |
| G4 | G | Q4 reconstruction preserves the canonical shell/permutation structure when raw Q4 placements do not determine a cell. | G3, T1 |
| T2 | T | Q4 reconstructs to the `p/g` selector family with control cores `110/220/212` and baseline `210`. | G3, G4, T1 |
| G5 | G | First recursive application substitutes selector depth into the primary address: `(q,d,j)->(q,S(j),j)`. | T1, T2 |
| T3 | T | First recursion has exactly three functional outputs, indexed only by `p`; hidden-state rank falls 14→3. | G5, T1, T2 |
| T4 | T | Operational compatibility yields the request/grant relation `00->1, 01->0, 10->2, 11->{0,2}`, equivalently eligibility `[X,NOR(X,Y),Y]`. | T3 |
| T5 | T | `210` supplies route reindex `q=2-p`; Q3 completes to `102/012/120`. | T3, T4 |
| G6 | G | The same selector is reused on the regenerated surfaces: `(q,S(j),j)->(S(j),S(j),j)`. | T2, G5 |
| T6 | T | Second reuse canonicalizes every legal state to frame 9 / payload `100` / raw `---//////`; hidden-state rank falls 3→1. | G6, T3, T5 |

The present transition-side supplied set is therefore **O1–O2 + G1–G6**. Everything T1–T6 is downstream and must not be counted as independent evidence for those premises.

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

1. **G1/G2:** broaden the primary POS3 + no-self parent family and measure how strongly the corpus selects it.
2. **G4:** isolate exactly how much Q4 reconstruction uniqueness depends on canonical-shell preservation.
3. **G5/G6:** test nearby address-substitution and selector-reuse families without presupposing the current recursion.
4. **T7–T11:** reproduce the complete machine in an implementation that never uses the Boolean `XYZG` representation.
5. **R1:** keep observer evidence quarantined when auditing transition uniqueness.

Experiment 241 does not change the preferred machine. It sharpens the frontier by identifying six genuine transition-side grammar commitments and makes the state-language conversion explicitly downstream of the request/grant relation.
