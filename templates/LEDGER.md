# Ledger

The open list of fixes. Release rules are in `RELEASE_PROCESS.md`.

## How it works

- **Everything here must be addressed.** An item leaves only when it's fixed in a released version or the owner drops it.
- **What goes in:** every fix the owner says needs doing, every review finding not fixed in the version that found it, and each version's scope while it's being built.
- **What doesn't:** feature ideas and anything not yet clarified go to `BACKLOG.md`, with the owner's approval.
- **Removing items:** when a version ships, its scope and the items it fixed are removed. Git history keeps the record.
- **Each item** has an ID, a plain description, and where useful the code location, evidence (VERIFIED or TRACED) and how often users can hit it.
- **IDs:** next free are **F-001** and **D-001**. Whoever assigns one updates this line in the same commit; IDs are never reused.

## Current version

### <version> (owner: "<their words for the goal>")

1. **F-###, <short name>** (D-### if a decision governs it). Done means: <what must be true when it's finished>.

Real-world test additions: <checks for what this version touches>.

## Open items

### <Area>

- **F-###** (<where it came from>): <the problem, where in the code, VERIFIED or TRACED, how often users can hit it>.
