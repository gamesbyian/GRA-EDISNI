# Retail INSIDE game consumer: offline binary reconnaissance

_12 October 2026. DISCOVER/DEVELOP. No retail gameplay assembly was available for this PR; no sticker decoder, CE password, accepted Steam beta code, or new native game input has been discovered._

## Why managed code before Ghidra?

The existing [game-code/source inventory](game-code-reverse-engineering-sources.md) includes a Cheat Engine/Mono table targeting **Windows Steam INSIDE v5.0.4**, with the managed runtime method `CameraBlendProbe:UpdateWeightsPosition`. A separate [2026 community binary audit](https://www.reddit.com/r/PlaydeadsInside/comments/1sqij1h/nearly_10_years_on_a_codelevel_audit_of_insides/) asserts `PrintingPaperEasterEgg` and `SecretType` exist in the retail PC/macOS builds. **Those specific class assertions are unverified by this repo.**

For authenticated **managed** `Assembly-CSharp.dll` input, [ILSpy](https://github.com/icsharpcode/ILSpy/blob/master/ICSharpCode.ILSpyCmd/README.md) is the appropriate starting point. Use [Ghidra's documented headless analyzer](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/RuntimeScripts/support/analyzeHeadlessREADME.md) on a suitable **native** target such as a verified IL2CPP GameAssembly, rather than assuming a native executable contains the puzzle's C# logic.

Important distinction: Steam's beta-branch password prompt is part of the **Steam client**, and an absence of matching game-local methods would not falsify the exploratory Steam branch in [PR #181](https://github.com/gamesbyian/GRA-EDISNI/pull/181). Do not send candidate passwords to live Steam or third-party endpoints.

## Local-only intake

This repository does **not** contain a legally acquired retail executable or `Assembly-CSharp.dll`. To study one, use an installed game that you control. Preserve storefront/build labels, acquisition date and file provenance alongside the generated SHA-256 hashes.

```sh
python scripts/consumer_binary_intake.py --root '/path/to/INSIDE' --output '/outside/repo/inside-consumer/intake.json'
```

The scanner reads a bounded list of recognizable file names and emits only relative paths, file sizes, SHA-256 hashes and header classifications. It skips symlinks and does not send bytes to any service. PE/CLI signature checks are intentionally limited: a signature is neither a guaranteed loadable assembly nor proof of a version.

With a verified managed `Assembly-CSharp.dll` and an independently installed `ilspycmd`, the combined local pipeline is:

```sh
bash scripts/run_local_consumer_recon.sh '/path/to/INSIDE' '/outside/repo/inside-consumer'
```

It produces `intake.json`, locally decompiled C# under `decompiled/`, and metadata-only `candidate-hits.json`. The C# never enters Git. The **pre-frozen** source-search groups cover historically reported printer terms, original lever/bunker interactions and plausible validation/state-transition names; each hit is recorded by path, line, marker and source-file hash, not source text. Hits require manual inspection.

For authenticated native targets, a local Ghidra installation can run the optional native string/cross-reference report:

```sh
GHIDRA_HOME='/path/to/ghidra' bash scripts/run_ghidra_consumer_local.sh \
  '/path/to/GameAssembly.dll' '/outside/repo/inside-consumer/native-candidates.csv'
```

`scripts/ghidra/InspectConsumerStrings.java` records addresses, bounded matched marker names and cross-reference counts, not string values. **This Java script has not been exercised against an installed Ghidra runtime or original INSIDE binary**, so actual runtime compatibility remains a test gate.

## Scientific stopping and promotion criteria

1. **Artifact:** original executable or managed assembly obtained from a lawful source, with size, SHA-256, platform and exact version documented. The current scripts have no such retail input.
2. **Mechanism:** confirm the proper managed/native path, then identify a specific class/function or original external form that receives user-controlled input. An enum name or string occurrence alone is not enough.
3. **Acceptance:** trace the full input/state transition and separately demonstrate accepted and rejected inputs in the appropriate offline or local environment. Distinguish the already solved 14-orb lever and printer paths from a genuinely additional consumer.
4. **Sticker linkage:** show an independently established foreground-to-consumer operation. Do not infer a CE decoder from a generic word, named class, or conveniently shaped interface.

If no retail assembly is accessible, the correct output is **no receiver authenticated**; do not substitute synthetic fixtures for source evidence.

## Tests and scope

```sh
python scripts/test_consumer_binary_intake.py -v
python scripts/test_decompiled_consumer_hits.py -v
bash -n scripts/run_local_consumer_recon.sh scripts/run_ghidra_consumer_local.sh
```

The six Python tests are synthetic: managed/native PE signatures, incomplete PE rejection, UnityFS/ELF detection, SHA-256 metadata, symlink exclusion, absent IL2CPP metadata, anchored managed-code keyword matches and refusal to export source text. They establish tool behavior only, not that game reverse engineering succeeded. A narrow CI job repeats them without downloading, installing, or analyzing an INSIDE binary.

**Next experiment:** a source-authorized local Windows install would allow authenticating the claimed `PrintingPaperEasterEgg` / `SecretType` witness and identifying any *additional* code-entry/secret-selection execution path. The consumer-first plan from merged [PR #182](https://github.com/gamesbyian/GRA-EDISNI/pull/182) remains in effect, with OR-Tools benchmarks as a separate subsequent task.
