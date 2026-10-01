# INSIDE game-code and reverse-engineering sources

Acquired 2026-10-01 for the sticker/ARG research corpus.

## Community reverse engineering: abarichello/inside-noclip

Pinned upstream commit: `027c79f03585ab61a8b6403c4480939a30162a02`

Source: https://github.com/abarichello/inside-noclip

License: GPL-3.0 (upstream LICENSE preserved)

What it is:
- Cheat Engine table for Steam INSIDE v5.0.4.
- Lua helpers and Auto Assembler patches for camera/player manipulation.
- Runtime addresses and managed-method names, including `CameraBlendProbe:UpdateWeightsPosition`.
- Evidence that the shipped Windows build exposes Mono-managed code paths and symbols useful for deeper reverse engineering.

What it is not:
- A full game-source release.
- A complete decompilation.
- Direct evidence for the Collector's Edition sticker mechanism.

Research value:
- Gives known-good runtime hooks and class/method names for validating future managed-assembly inspection.
- Provides a concrete starting point for scene/camera exploration around in-game ARG objects.
- Can help cross-check whether decompiled class names/methods correspond to known working runtime patches.

## Official released INSIDE source: playdeadgames/temporal

Pinned upstream commit: `4795aa0007d464371abe60b7b28a1cf893a4e349`

Source: https://github.com/playdeadgames/temporal

License: MIT (upstream LICENSE preserved)

Playdead describes this repository as the source-code release of the temporal reprojection anti-aliasing solution used in INSIDE. The vendored subset contains the main C# runtime components plus the temporal-reprojection and velocity-buffer shaders.

What it is:
- Genuine Playdead-authored C# and shader source used by INSIDE.
- Useful for code-style, Unity-version, rendering architecture, naming, and engine-integration context.

What it is not:
- General gameplay source.
- ARG logic source.
- A substitute for inspecting the shipped managed assemblies.

## Search status

A public full `Assembly-CSharp` decompilation or broader community source reconstruction was not found in the 2026-10-01 GitHub/web pass. The community noclip project is the strongest game-specific public reverse-engineering artifact found so far.

Because the noclip table references `mono.dll` and managed method names, a future controlled extraction/decompilation pass from a legitimately obtained INSIDE install is likely worth doing. That should be treated as a separate evidence-acquisition lane and should preserve exact game version/build provenance.
