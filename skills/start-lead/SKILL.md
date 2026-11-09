---
name: start-lead
description: PM procedure to start a Lead session for a version (or a tooling or website task) once the owner says to start, and to add items to a running version. Covers numbering, pre-start checks, the brief template and checking the Lead's report.
---

# Start a Lead

The owner and PM settle the scope together; when the owner says "start" (or similar), the PM starts the Lead without showing the brief first. Roles and rules: `CLAUDE.md` "Operating model"; release work: `docs/RELEASE_PROCESS.md`.

## 1. Number it

Give each Lead a number and a short title, e.g. `L-042 — 1.3.0`. Use the next number after the highest used anywhere (commit messages, branch names, the ledger), since commits alone miss Leads that never committed.

```bash
{ git log --all --format='%s%n%b'; git branch -a; cat docs/LEDGER.md; } | grep -oE 'L-[0-9]+' | sort -t- -k2n | tail -1
```

## 2. Check before starting

- The scope is in `docs/LEDGER.md` under "Current version", each item with a "done means" line.
- Every item went through the scoping rule in `docs/RELEASE_PROCESS.md`, and the owner has decided everything it raised.
- No other code-writing session works in the same checkout; otherwise start this one in its own worktree.
- The machine can do what the work needs (devices connected, signing and release setup, deploy access). Tell the owner what's missing instead of starting a Lead that will block.

## 3. Brief template

Make it complete enough that the Lead doesn't rediscover strategy; point to docs instead of copying them.

- **Goal:** one or two sentences.
- **Scope:** each ledger ID with its done-means, in the owner's words. Nothing else.
- **Phases and gates:** e.g. "investigate F-057 and report to the PM before any code".
- **Pointers:** `CLAUDE.md` sections, `docs/CODE_MAP.md` subsystems and decision IDs the work touches; earlier commits worth reading.
- **Limits:** what the Lead may and may not touch (test devices and accounts only, never the owner's own copy); never widen scope (findings go to the PM for the ledger); decisions change only with the owner's approval, through the PM.
- **Choices during the build:** a choice the scope didn't settle follows the docs that already decide it; only one they don't clearly answer goes to the PM (`docs/RELEASE_PROCESS.md`, Build step).
- **Findings:** every finding, from any review, audit or test, passes the finding gate before it reaches the PM; nothing is fixed before the owner's triage.
- **Release:** follow `docs/RELEASE_PROCESS.md` through the real-world test and Record (run the docs-audit checker before handing in Record); ship only after the owner's explicit approval in the Lead's own session.
- **Workers:** a mid-tier model by default, the smallest model for read-only search, the strongest only where a Worker has failed at the judgment.
- **Report:** what changed; VERIFIED (tests, real runs) vs TRACED (code reading); open questions; net line delta; branch, commits and push state. Stop when done or blocked.

## 4. Start it

Start a fresh session with the title and brief. Note its session ID for follow-ups.

## 5. Items added after the start

Adding items mid-version is normal, but only when the owner explicitly adds one. Run the scoping rule first and bring the owner what needs them. Then record the item in the ledger's current version, with its done-means, and send it to the running Lead, saying where it fits in the phases. Don't start a second Lead for it unless the owner wants it in parallel (then use a separate worktree).

## 6. When the Lead reports

Check its claims against the code, ledger and decisions before passing them on; label anything unverified. Bring the owner only their decisions, concisely.
