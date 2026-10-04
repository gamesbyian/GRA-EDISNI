# Experiment 411 — complete Terminal41 typed-input inventory

_Status: completed source-tree audit, 4 Oct 2026._

The external-consumer program keeps returning to Terminal41 because the ARG demonstrably used web endpoints and state transitions.

That makes one question worth answering exhaustively:

> does the preserved Terminal41 snapshot itself expose any typed input interface that could consume the sticker outputs?

## Corpus

The vendored Terminal41 source-tree manifest contains:

```
74 files total
73 text-or-unknown files
1 binary-media file
```

All 73 text files were scanned.

The audit looks specifically for HTML interface grammar:

- `<form>`
- `<input>`
- `<select>`
- `<textarea>`

It also inventories button tags separately while distinguishing ordinary navigation/redirect pages.

## Result

Across the complete preserved text snapshot:

```
form      0
input     0
select    0
textarea  0
```

The archive contains:

- static state/status pages;
- path-based transitions;
- meta-refresh redirect chains;
- directory indexes;
- fixed links.

It does **not** preserve a nine-value, ternary, numeric, or free-text entry surface inside Terminal41 itself.

## Important scope limit

This does not mean the overall ARG lacked typed consumers.

It demonstrably did.

Historical printer JavaScript and the Playdead-site subscription-box workflow accepted solver answers and unlocked later material. Those consumers live outside this static Terminal41 snapshot and are already documented in the external-consumer audit.

The distinction matters:

> Terminal41 preserves state and routing structure; the known answer-entry grammar lived elsewhere.

## Consequence for the sticker mystery

The current live derived interfaces include:

- one-shot E2;
- `--/--/-/-`;
- the 9+3 numeric surface;
- the serial-digit outputs from Experiment 410.

None can be responsibly “entered into Terminal41” because the preserved Terminal41 corpus supplies no input grammar for doing so.

This closes a large class of tempting URL/path spraying.

## Next consumer target

Search should now favor artifacts that actually preserve an interface grammar:

- historical Playdead-site JavaScript;
- answer-validation requests;
- explicit printed/packaging instructions;
- structured files that define selectors or lookups.

Static Terminal41 path resemblance alone is insufficient.
