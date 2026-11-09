# Ledger

The open list of fixes. Release rules are in `RELEASE_PROCESS.md`.

## How it works

- **Everything here must be addressed.** An item leaves only when it's fixed in a released version or the owner drops it.
- **What goes in:** every fix the owner says needs doing, every review finding not fixed in the version that found it, and each version's scope while it's being built.
- **What doesn't:** feature ideas and anything not yet clarified go to `BACKLOG.md`, with the owner's approval.
- **Removing items:** when a version ships, its scope and the items it fixed are removed. Git history keeps the record.
- **Each item** has an ID, a plain description, and where useful the code location, evidence (VERIFIED or TRACED) and how often users can hit it.
- **IDs:** next free are **F-004** and **D-003**. Whoever assigns one updates this line in the same commit; IDs are never reused.

## Current version

### 1.2.0 (owner: "<their words for the goal>")

1. **F-001, routine popups look like errors** (D-002). Done means: popups that aren't failures are titled with their reason; real failures keep the error title.
2. **F-002, slow first launch.** Done means: first launch shows the main window in under 2 seconds on <reference machine>. Investigate first and report before code.

Real-world test additions: <checks for what this version touches>.

## Open items

### <Area>

- **F-003** (deferred from the 1.1.0 review): a cancelled sync can show a stale error for a moment. Safety net; TRACED (`src/sync/Sync.ts:120`).
