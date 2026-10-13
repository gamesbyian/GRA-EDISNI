# Consumer-first game-code evidence: method-shape and signal audit

_12 October 2026. DISCOVER/DEVELOP. No original retail gameplay assembly was available for this work; no CE foreground receiver has been demonstrated._

## Rationale

Our merged local binary intake and ILSpy pipeline already searches known method names. This leaves a blind spot: an unknown input validator might use no word like password, code, or secret in its name.

The [20 April 2026 community technical account](https://www.reddit.com/r/PlaydeadsInside/comments/1sqij1h/nearly_10_years_on_a_codelevel_audit_of_insides/) describes two allegedly related prefix-checking flows: PC SecretJoystick.CheckPassword and Switch PrintingPaperEasterEgg.InputCheckAndStateTransition. It reports a live PC printSecretMessage signal receiver, but no sender in the author's observed code. These are **third-party claims, not independently verified from shipped binaries here**. They offer a specific research strategy: look for input accumulation, prefix comparison and mismatch reset even in unfamiliar methods.

## Source-specific frozen verification targets

| Source claim | Appropriate original artifact | Proof required | Important competing explanation |
| --- | --- | --- | --- |
| PrintingPaperEasterEgg is the printer class | Windows PC Mono Assembly-CSharp.dll | Real source class and actual branch structure | Printer behavior already decoded |
| SecretJoystick.CheckPassword checks a sequence | Windows PC Mono | Method implementation and producer-to-handler path | Known 14-orb bunker password explains it |
| printSecretMessage is subscribed but not emitted | PC Mono **and original scene/signal assets** | Subscriber plus whole-program sender and invocation census | A limited .cs search cannot establish no native/scene/other-DLL sender |
| macOS Cutout has no local decoder | macOS 1.0.4 Mono | Case body, data references and complete callees | Manual/off-platform interpretation may still exist |
| Switch rrlrll consumes attachment changes | Switch IL2CPP | Original metadata, native input path, build provenance | Mono-only scan does not inspect IL2CPP |
| Steam beta password is a consumer | **Steam client**, not gameplay DLL | A branch associated with an independently derived sticker input | Missing gameplay code cannot falsify Steam functionality |

The report's RVAs and inferred platform genealogy remain externally supplied statements until binary source hashes and actual code establish them. Its author had no Xbox dump.

## New structural auditor

The optional script at scripts/audit_managed_consumer_structures.py scans **locally decompiled C#**, with bounded file sizes and file counts. Within each lexically identified method body it looks for the conjunction of:

1. A length-sensitive input or buffer operation.
2. A prefix primitive: Substring, StartsWith, or Take.
3. Equality/inequality comparison.
4. Clear or reset action.
5. Symbol accumulation.

It separately tags named historical methods and an exact quoted printSecretMessage literal, with comments masked. It returns relative file paths, SHA-256 digests, line spans and feature booleans. It never exports proprietary C# statements or password values.

This is a **heuristic research triage**, not proof of a validator. It has known false-negative territory: native/IL2CPP code, expression-bodied methods, unusual interpolated/raw strings, indirect comparisons, recursion/array-index validators, engine scene events and unsubscribed code. A syntactic hit is not a reachable input. Absence of hits is not evidence that every game build lacks a code consumer.

Run the integrated local pipeline:

    bash scripts/run_local_consumer_recon.sh '/path/to/INSIDE' '/outside/repo/inside-consumer'

It produces intake.json, candidate-hits.json, structural-candidates.json and decompiled sources under a **user-selected directory outside the repo**.

Or scan an existing local C# tree:

    python scripts/audit_managed_consumer_structures.py --source-dir '/path/to/decompiled' --output '/outside/repo/structural-candidates.json'

The six synthetic tests exercise unfamiliar method names, comments and literals, cross-method nonmatches, signal references, missing paths and symlinks. They test our scanner, not INSIDE.

## Promotion criteria

For any discovery require exact source and build provenance; input producer/event; the full handler's guards and callees; locally demonstrable accepted/rejected behavior where possible; and, separately, a source-grounded sticker-to-consumer mapping with preregistered controls. The entire receiver branch remains exploratory until those links exist.

No Playdead contact, new sticker, website password spraying or proprietary game upload is necessary for this *research-tool* improvement. Authentic retail game code remains a future evidence dependency for using the tool to make gameplay claims.
