# Mechanical theorem graph

_Status: Experiment 241 theorem graph, now paired with the executable proof pack in `scripts/verify_proof_pack.py`._

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
| G3 | G | Each Q4 depth stack uses POS3 locally. The executable canonical path fixes the all-slash shared-polarity representative as a gauge convention; global shared polarity is not asserted as a functional necessity. | O2 |
| T2a | T | Raw Q4 observations force the shared exceptional symbol to slash (36 compatible slash-exception completions, zero dot-exception completions), yielding exactly 36 selector completions. | O2, G3 |
| G5 | G | First recursive application substitutes selector depth into the primary address: `(q,d,j)->(q,S(j),j)`. This operation is defined on the raw POS3 candidate space and does not depend on the completed primary lattice. | O2, T2a |
| T0 | T | Under G1, raw observations force 8/9 primary frame polarities. Testing both locally valid polarities at `q=1,d=2` through G5 leaves 20 first-pass survivors for slash-minority and zero of 432 alternate-polarity candidate machines. Therefore all nine frame polarities are derived and equal the staircase `minority dash iff d<=q`. | O2, G1, T2a, G5 |
| T1 | T | Under G1 and derived polarity T0, raw observations force 25/27 primary payload trits; the only unresolved trits are `x=(q0,d2,c1)∈{1,2}` and `y=(q2,d0,c1)∈{0,1,2}`. | O2, G1, T0 |
| T1a | T | All 18 outer primary trits are observation-forced and satisfy minority-row `!=d`; the old outer no-self rule is therefore derived rather than an additional premise. | T1 |
| T1b | T | The primary payload family reduces to `112 212 0x0 / 212 002 100 / 1y2 022 100`, with the route/cross normal form described in current-state. | T1, T1a |
| T3a | T | Cartesian product of the 6 raw-compatible primary payloads and 36 raw-compatible selectors gives 216 candidate machines; first-pass POS3 closure leaves 20. | T1b, T2a, G5 |
| G6 | G | The same selector is reused on the regenerated surfaces: `(q,S(j),j)->(S(j),S(j),j)`. | G5 |
| T2 | T | Second-pass POS3 closure reduces 20→14 and reconstructs the Q4 control family: C is a free {0,2} gauge and A/D/G cores are exactly `110/220/212`. | T3a, G6 |
| T3 | T | The 14 survivors have exactly three first-pass functional outputs; hidden-state dependence falls 14→3. | T2, G5 |
| T4 | T | The request/grant relation `00->1, 01->0, 10->2, 11->{0,2}`, equivalently eligibility `[X,NOR(X,Y),Y]`, emerges from surviving primary ports versus the three reconstructed control cores. | T2, T3 |
| T5 | T | Among all 27 ways to select one q-indexed output from each of the three T3 functional families, requiring three distinct ternary permutations uniquely selects choices `(2,1,0)`, equivalently `q=2-p`, and route shell `120/012/102`. | T3 |
| T2b | T | If Q4 stack polarities are freed independently under local POS3, raw observations admit 256 polarity words; recursive closure leaves 16, maximum 14-state retention leaves 8, and the T5 reversible-route criterion leaves exactly `0`, `A`, `C`, and `A+C`. Those four differ only by unobserved A/C physical gauges and share route shell `120/012/102` with terminal `100`. | O2, G3, T1b, G5, G6, T5 |
| T6 | T | Every one of the 14 canonical-representative second-pass survivors canonicalizes to frame 9 / payload `100` / raw `---//////`; T2b confirms the same endpoint across the full route-capable independent-polarity gauge orbit. In the broader maximum-retention nonlinear recursion family, `100` is also the unique terminal surface fixed under another selector application, while `102` moves to `100`. | T2, T2b, G6 |

Taking the two recursive operations G5–G6 as the operation grammar, the present transition-side supplied set is **O1–O2 + G1 + local-Q4-POS3 G3 + G5–G6**. The all-slash shared-polarity form used by the canonical executable path is now explicitly a gauge fixing, not a functional premise. Experiment 292 removes global shared polarity from the functional claim: independent stack polarities collapse under recursive closure plus T5 to the four exact A/C gauge representatives with the same route shell and terminal. Experiment 277 removes the former G2 staircase premise: eight primary frame polarities are directly forced by raw marks under POS3, and first-pass recursive viability uniquely fixes the ninth. Experiment 254 remains the representative-level observation that, if one directly imposes a shared Q4 polarity, raw data force slash-exception. Experiments 250–252 remove the former Q4 canonical-shell reconstruction premise from the minimal generation chain: the surviving Q4 scaffold/control family is recovered by closure from the 36 raw selector completions. The former outer no-self grammar is likewise theorem-level.

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

Experiment 257 shows that direct exact-POS3 occupancy is not the only compact route back to those 14 states. Inside the 832-state optional-pulse closure family, require only that the three depth frames within each external quarter have equal total pulse count. That coarser quarter-local balance condition leaves exactly 14 states, all with frame weight 3 and therefore with every primary column occupied.

Experiment 271 tests whether the quarter grouping is itself being smuggled into that result. Across all 280 partitions of the nine frames into three triples, 90 abstract balance partitions recover the 14-state family. However, the native 3×3 frame geometry has only two partitions into three straight parallel rails: q rows and d columns. Quarter rows recover 14 states; depth columns leave 50. The quarter-local balance rule is therefore unique inside the visible straight-axis partition family, though not among arbitrary nonlocal equality groupings.

Experiment 272 then removes the optional-pulse column parent itself and requires only three minority cells somewhere in each 3×3 frame. Raw observations permit 1,296 such primaries; recursive closure with the 36 selectors leaves 1,548 states, every one still terminating at `100`. Exactly 14 of those states have one minority cell per physical column. This establishes a sharper boundary: frame-level population symmetry is enough for endpoint robustness but not for the exact physical family, so some directional rail structure remains genuinely load-bearing for G1.

Experiment 273 adds only horizontal first-moment centering to that broader parent. Because three pulses with centroid at the middle column can be either distributed `(1,1,1)` or piled `(0,3,0)`, this is strictly weaker than G1. Recursive closure leaves 28 states: 14 canonical exact-POS3 states and 14 siblings differing only at `q=1,d=0`, where the three pulses occupy the centre column. The fork lives entirely at four unobserved residues, 28/33/34/35, and both branches terminate at `100`. This isolates the remaining local G1 assumption to a single distributed-versus-centre-pileup physical choice.

Experiment 274 supplies a corpus-facing discriminator for that fork without reading solved payloads. After normalizing observed symbols to minority/majority, exactly two frame pairs maximize conflict-free raw support at four shared observations and eight-of-nine union coverage: `q0,d1=q1,d0` and `q1,d2=q2,d2`. Requiring both partial-repeat hypotheses to extend to exact frame repeats selects exactly the canonical 14 states from the 28-state centroid parent. The pileup sibling preserves the second repeat but violates the first. The remaining assumption is therefore narrower than full G1: promote the two strongest raw-compatible frame repeats to exact local repetition.

Experiment 275 provides an independent structural discriminator. Prior to recursion, the canonical and pileup branches each contain the full six-element `x×y` primary Cartesian product. Canonical closure preserves all six primary projections. Pileup closure removes exactly `(x=1,y=2)` and reaches the same total of 14 states only by increasing multiplicity on other primary coordinates. Thus the canonical branch uniquely preserves the raw primary coordinate domain through closure; the sibling introduces a cross-layer exclusion not demanded by the primary observations.

Experiment 276 shows that the sibling is also operationally degenerate. Across its 14 physical states the first recursive pass has rank 1, always yielding `102/022/100`, and selector variation survives only at C/G. The canonical branch has rank 3 with the three functional outputs already used by T3/T4 and retains A/C/D/G selector variation. Therefore equal terminal and equal physical state count do not make the sibling an equivalent transducer: only the canonical branch preserves a nontrivial intermediate control quotient.

Therefore G1 has three distinct statuses:

- **raw parent:** zero-or-one pulse per column is a broader tested grammar;
- **exact-state selection:** direct exact POS3 or the weaker quarter-local frame-weight balance both recover the canonical 14-state family inside that parent;
- **endpoint robustness:** even without either exact-state selector, all 832 recursively closed states terminate at `100`.

This distinction prevents overclaiming uniqueness while strengthening the terminal's robustness.

Experiment 280 adds a second distinction: **transducer uniqueness versus physical-completion uniqueness**. Inside the frame-weight-three parent, four occupancy families reproduce the canonical operational invariants exactly. They are generated by two independent fixed-cell moves: H↔F in frame q0,d0 (residues 8↔6) and I↔E in q1,d1 (45↔41). The affected residues are unobserved, and the corresponding selector values make those frame/depth cells unreachable in every raw-compatible selector. Consequently no recursive transition evidence can distinguish these four physical representatives. Exact G1 column POS3 fixes the zero-gauge representative; the transition itself determines only the equivalence class.

Experiment 282 supplies an independent physical regularity on that equivalence class. Using only the 3×3 `(q,d)` frame geometry, define the cost between adjacent frames as minimum Manhattan transport between their three minority cells. The two gauge flips independently increase transport at their affected neighborhoods, and the zero-gauge exact-POS3 representative uniquely minimizes aggregate transport across all six raw primary `(x,y)` payloads. This selects the same physical representative without inspecting selector reachability, recursive outputs, or column occupancy. The selection remains simplicity-level rather than observation-level evidence.

Experiment 283 removes dependence on one exact distance choice. In the metric family with orthogonal step cost 1 and diagonal step cost λ∈[1,2], exact lower-envelope enumeration over all token matchings shows the zero gauge is uniquely cheapest for every λ>1. At λ=1 the q1,d1 flip ties, but q0,d0 remains excluded. Therefore the transport preference is robust across the natural metric continuum except for one boundary degeneracy.

## Q4 polarity boundary

Experiment 256 enumerates every slash-exception/dot-exception assignment over the nine Q4 stacks. Raw marks allow 256 of the 512 polarity words. Only 16 survive recursive closure:

- 8 maximal words retain 14 states and terminate at `100`;
- 8 sibling words retain 12 states and terminate at `110`;
- the remaining 240 raw-compatible polarity words admit no recursively closed state.

Across every maximal 14-state word, B/D/E/G/H are forced slash-exception. A/C/F/I vary across the maximal family. Experiment 260 factorizes that variation exactly: the maximal family is a 3-bit XOR gauge cube generated by independent A and C polarity flips plus one coupled F+I flip. The 12-state/`110` sibling family is precisely the same gauge cube with D polarity toggled.

Thus the globally shared-polarity form formerly attached to G3 is sufficient but not minimal for the transition. G3 now means only local Q4 POS3 plus an explicit canonical gauge choice for the executable representative. Experiment 292 closes the functional ablation: after independent polarities, recursive closure and the already-derived route criterion retain only `0/A/C/A+C`, all exact A/C physical gauges. Any claim that the full printed Q4 surface is uniquely reconstructed must still identify an independent reason to select the all-slash gauge origin.

Experiment 270 supplies a bounded physical-simplicity discriminator for that gauge choice. Among all 16 recursively closed polarity words, the all-slash word is uniquely minimal in four geometry-only costs on the actual 3×3 artwork: flipped-stack count, orthogonal domain walls, mixed rows, and mixed columns. This does not promote simplicity to observation-level evidence, but it shows the authored completion is the unique globally homogeneous representative of the gauge orbit. Combined with Experiment 254, the compact authoring grammar "one shared Q4 exceptional-symbol polarity" selects slash from raw data and lands exactly on that zero-gauge representative.

Experiment 281 supplies a second physical discriminator that is global rather than local. The primary contributes a fixed 45 slash / 36 dash under exact POS3. Every dot-exception Q4 stack increases slash count by one and decreases dot count by one relative to all-slash. Hence only the zero-gauge Q4 word yields the complete-master census `54/36/18 = 3:2:1`; this is unique across all 256 raw-compatible polarity words. Local homogeneity and global alphabet balance therefore select the same Q4 representative independently.

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

1. **G1:** Experiments 257/271 reduce the frame-balance side; Experiments 272–276 reject the obvious centre-pileup sibling; Experiment 277 removes G2 entirely. Experiment 280 proves a hard two-bit physical gauge at unobserved, selector-unreachable residues 6↔8 and 41↔45. Exact POS3 fixes the zero gauge but transition evidence cannot. Experiments 282–283 independently favor that same representative by local transport, robust for every natural diagonal cost λ>1; at λ=1 only the q1,d1 bit remains tied. Further G1 work should seek a second non-transport cue for q1,d1 or archival/manufacturing evidence for the unreachable cells.
2. **G3:** Experiment 292 removes global shared Q4 polarity as a functional requirement. With only local POS3 and independently free stack polarity, closure plus the T5 route criterion leaves `0/A/C/A+C`; Experiment 289 proves A/C are exact unobserved physical gauges. Experiments 270 and 281 independently select all-slash as the preferred printed representative by local homogeneity and the unique `3:2:1` complete-master census, while Experiment 254 shows raw data force slash if shared polarity is imposed directly. The remaining issue is only the physical gauge origin, not the route computation.
3. **G5/G6:** Experiment 266 extends first-pass G5 to all 432 coupled affine bijections of the `(q,S)` plane. Maximum raw-state retention still forces `d'=S` and leaves only external-q relabeling; Experiment 267 shows singular maps win only by erasing S. Experiment 278 fixes the downstream Q3 orientation without importing `210`. Experiments 279/284 select `100` by true fixed-point behavior and reject the period-2 `102↔100` branches. Experiment 285 then proves the sole remaining stable `f_1` swap is an exact observational gauge: it acts only at A/D/F when S=1, and q0,d1/q1,d1 store identical symbols at those cells. Further recursion broadening should therefore quotient this gauge rather than mistake it for an unresolved behavioral branch.

Experiment 286's claimed `Z2^6` direct product is superseded. It changed Q4 polarity without re-solving the exceptional depth, which is not a valid physical completion. Experiment 287 performs the joint enumeration correctly. The exact canonical-transducer gauge has four physical bits: the two primary completion bits plus Q4 A and C polarity bits, giving 16 physical settings / 224 complete masters. The `f_1` operation gauge adds one exact-invisible bit, so the exact-transducer quotient has five bits / 32 representation settings. The Q4 F+I polarity branch is not an additional independent gauge: it is incompatible with the primary q0,d0 flip and, when viable, changes the intermediate first-pass words while retaining 14 states, rank 3, and terminal `100`. The broader recursive family contains 24 physical settings / 336 masters and 48 representation settings including `f_1`.

Experiment 288 separates that nearby branch from the exact functional quotient using the already-established Q3 theorem. The F+I first-pass families contain reversible-word sets `{"102","120"}`, `{"102"}`, and `{"102"}`. Hence no choice can yield three mutually distinct ternary permutations, whereas the canonical families uniquely yield `120/012/102`. This failure is invariant under every global ternary relabeling. The F+I family therefore shares coarse rank/state-count/terminal invariants but does not preserve the canonical reversible route structure.

Experiment 289 explains why Q4 A and C, unlike F+I, remain inside the exact quotient. Both corresponding Q4 stacks are completely unobserved, and switching their exceptional-symbol polarity leaves the surviving selector-depth set exactly unchanged. Since the recursive machine consumes selector depth rather than the printed slash/dot polarity, A/C change physical marks only and induce no transition change. Their physical supports are A={82,91,100} and C={84,93,102}.

Experiment 290 supplies a human-scale derivation of G5 inside the literal coordinate-copy family. Of `(q,q)`, `(q,S)`, `(S,q)`, and `(S,S)`, only `(q,S)` both depends on `S`, preserves external-q structure, and yields more than one valid output family. The alternatives are respectively selector-blind/rank-1, impossible, and q-collapsed/rank-1. This does not replace the broader uniqueness audits of Experiments 245/266, but it explains why the canonical substitution is discoverable without arbitrary-map search.

Experiment 291 gives G6 the same human-scale derivation. After G5 has produced 20 valid q-indexed machines, fixed q choices 0/1/2 keep all 20 and each leave three output payloads. Setting q=S is uniquely both selective and completion-invariant: it leaves 14 valid machines and one payload, `100`. Thus the simple address-copy family discovers both recursive substitutions without terminal targeting.
4. **T7–T11:** the lower-level constraint/enumeration target is now satisfied by Experiments 250–251; use it as the preferred independence oracle for future state-family changes.
5. **R1:** keep observer evidence quarantined when auditing transition uniqueness.

Experiment 241 created the graph; subsequent hardening through Experiment 278 has removed outer no-self, the ninth-frame polarity completion, a separately supplied Q4 scaffold/control reconstruction, and the Q3 `q=2-p` orientation from the premise set. The state-language conversions remain downstream descriptions of the 14-state closure family.
