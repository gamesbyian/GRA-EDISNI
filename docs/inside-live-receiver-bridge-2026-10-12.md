# INSIDE live game-code reconnaissance through InsideDevTool

Status: 12 October 2026, DISCOVER/DEVELOP. New upstream tool and offline collector; no authenticated INSIDE runtime capture or CE decode yet.

## Newly available instrument

[RedMatterGG/InsideDevTool](https://github.com/RedMatterGG/InsideDevTool), publicly uploaded to [Nexus Mods on October 7, 2026](https://www.nexusmods.com/inside/mods/8), is an MIT-licensed, purpose-built editor/inspector for INSIDE on Windows, targeting Unity 5.0.4f1.

Source pinned at upstream commit bdc3bbd7d61f1eb77f9e01200493c14c5ac2650a (Oct 7).

Its source describes:

- An in-game object browser and component inspector, scene and trigger inventory, PlayMaker FSM graph, event monitors and signal-input listing.
- A code dependency graph, built from loaded Assembly-CSharp and Assembly-CSharp-firstpass runtime types and method IL. The graph records callsites, field reads/writes, signal subscriptions and method entrypoints, conditional on the built-in parser's coverage.
- The bridge command logic <TypeName> queries a code graph; the gamecode command reports game-code presence.
- An MCP listener that binds 127.0.0.1:47811 by default, exposing structured read-only object queries and separately non-read-only tools for commands, edits, signal firing and FSM driving.

Source audit: upstream README, src/InsideDev/Runtime/CodeGraph.cs, src/InsideDev/Runtime/CodeDeps.cs, src/InsideDev/Remote.cs, src/mcp/Extension.cs, src/mcp/McpServer.cs, src/loader/version_proxy.c.

IMPORTANT CORRECTION to previous plans: upstream states that INSIDE's proprietary gameplay assemblies are **not ordinarily loose DLL files** in the shipped installation; its mod reads in-memory types while the game runs. The earlier offline Assembly-CSharp file intake is therefore optional and not necessarily feasible from an ordinary retail directory. The new route avoids requiring decompiled DLLs, although a lawful locally installed Windows game is still needed.

The source demonstrates implementation, not that the mod works on every retail version. No one here has yet executed the mod or observed a genuine signal/call graph.

## Security boundaries

The mod's version.dll is an injected proxy loader. Source includes runtime hooks and an optional local debugger agent on 127.0.0.1:55555. Its MCP API also has dangerous operations: set_active, fsm, signal and a command tool that accepts arbitrary console instructions. Its localhost binding and Origin check do not provide an authenticated sandbox. No automatic installation or antivirus exclusion is justified by this research.

If someone with a game installation elects to use it, first review the upstream source and prebuilt binaries, isolate the test environment, back up saves and avoid automatic cloud synchronization if appropriate. Treat full MCP access as powerful game-editing authority.

Our script scripts/acquire_insidedev_consumer_snapshot.py is standard-library only. It always sends to 127.0.0.1 and a fixed /mcp path. It does not install, download, launch or modify game code. It refuses to write a capture inside this repo, and never forwards the capture to GitHub or ChatGPT. It checks the server-reported identity, every call's readOnlyHint annotation, MCP message identifiers and result types. Note that the server name and tool hints are **self-reported**, not cryptographic guarantees.

The default capture contains seven upstream-advertised read-only inquiries:
- game_state;
- find_objects for Printer, SecretJoystick, WristSecret and generic secret scripts;
- fsm_find for printSecretMessage and Printer.

Example after independently reviewing and running the mod with a local game:

    python scripts/acquire_insidedev_consumer_snapshot.py --output "/outside/repo/insidedev/snapshot.json"

This batch does NOT fire signals, move objects, toggle states, invoke arbitrary commands or touch the original game binaries.

Deeper static code graph queries require the upstream MCP command tool, which is marked non-read-only. Accordingly the additional argument --with-logic is explicitly opt-in and restricts calls to exactly four fixed, inspection-oriented strings:

    gamecode
    logic PrintingPaperEasterEgg
    logic SecretJoystick
    logic shared secret

The logic type queries may open an editor panel and cause code scans. The script records that the non-read-only tool was used. It still refuses all arbitrary console text, game-editing commands and signal activation.

Example: 

    python scripts/acquire_insidedev_consumer_snapshot.py --with-logic --output "/outside/repo/insidedev/logic.json"

## What the snapshot should establish

1. Pin game version, platform, active scene and exact script/asset identities. A self-reported tool version is not original game-code provenance.
2. Locate the printer object and class. Check actual code dependencies and any subscription to printSecretMessage.
3. Search for independently reachable emitters in loaded code/scene, distinguishing per-scene negative evidence from an exhaustive game-wide absence claim.
4. Explore other sequence/check validation methods from discovered classes, without requiring that they be named Password or Secret.
5. Compare the verified receiver's native input alphabet, input length, ordering and successful response to raw physical sticker carriers without importing assumed ternary-machine predictions.

The [April 20 third-party decompilation report](https://www.reddit.com/r/PlaydeadsInside/comments/1sqij1h/nearly_10_years_on_a_codelevel_audit_of_insides/) reported a live printer receiver with no observed sender. This is a promising, falsifiable claim but remains externally reported. The known normal 14-orb password and printer functions already explain some real input consumers; any novel route must be independently distinguished. A local C# file-name search cannot falsify a Steam beta client password, because the latter belongs to Steam, not INSIDE gameplay code.

## Testing and evidence

The test script scripts/test_insidedev_consumer_snapshot.py runs a synthetic loopback MCP server and verifies session negotiation, allowlisted tool names, exact opt-in commands, changed safety annotations, unexpected server identity and output-path protection. The tests never launch the real game.

Results from the synthetic server certify only the collector logic. No gameplay executable, original signal, custom secret state or sticker-derived payload has been verified in this PR.

If the runtime prerequisite remains unavailable, maintain this workstream as a prepared path and continue the independently executable closed-corpus analysis in other lanes. More stickers and Playdead contact are not prerequisites.
