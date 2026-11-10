# CLAUDE.md template

The instructions file your coding agents read first. Copy it to your project root, replace the parts in angle brackets, and delete what doesn't fit your project.

---

# Repository instructions

These instructions apply to the entire repository.

## Mission

Build **<project>**, <one sentence on what it does and for whom>.

Prioritize correctness and user trust, maintainable implementation, and low support burden for a solo developer.

## Sources of truth

Use these as persistent project memory, in order:

1. `docs/DECISIONS.md`: the owner-approved rules that apply today, each linked to its code. It wins over every other document.
2. `docs/CODE_MAP.md`: how the code works per subsystem: flow, key files, invariants, where to start debugging.
3. `docs/GLOSSARY.md`: the shared terms. Use its words in code comments, briefs, reports and user-facing text.
4. `docs/RELEASE_PROCESS.md`: how every version is scoped, reviewed, tested and shipped. `docs/LEDGER.md` is the open list of fixes and the current version's scope.
5. `docs/BACKLOG.md`: owner-approved future ideas only.

Do not silently resolve conflicts between sources. Raise material conflicts to the owner.

Read only relevant sections. Point to files instead of copying their content into prompts and handoffs.

## Copy-ready text for the owner

Anything the owner may copy and paste (emails, commands, prompts for another agent, post drafts) goes in its own fenced code block, one block per item.

## Backlog rule

Add an idea to the backlog only after the owner explicitly approves that specific item. Discussion and agent suggestions are not approval. Backlog entries never expand a version's approved scope and are not commitments.

## Evidence discipline

Label accepted decisions, hypotheses, observed evidence and open questions distinctly. Do not present a hypothesis or limited evidence as universal behavior.

Before relying on how the product behaves, check the code or the decisions first; never assume from memory or plausibility.

Prefer primary documentation for public contracts. Verify undocumented behavior with reproducible tests, and report the environment, versions, procedure, result and limits. A fact future work relies on becomes a decision or a code-map "Must hold" line.

## Engineering principles

- Keep business logic deterministic and testable outside thin UI and platform adapters.
- Make validation proportional to the change and its risk. Check observable behavior at service boundaries; avoid tests that mirror the implementation.
- Test a safety rule through the real path that triggers it. A test that forces the condition directly (an override) can't catch bugs in how the condition is detected, so pair it with at least one test that runs the real flow.
- For new behavior, validate the smallest safe end-to-end slice before expanding it.
- Reuse or extend existing rules; allow focused duplication when it's clearer than an abstraction. No frameworks or infrastructure for unapproved features.
- One deterministic rule beats special cases. Remove over-strict checks. Prefer fewer lines.
- Treat writes, migrations and anything users can't undo as high-risk: handle errors and interruptions, back up first, and verify failure and recovery behavior before release.
- Minimize dependencies; review third-party code for security and license compatibility.
- For nontrivial bugs: establish evidence, isolate the responsible stage, test the smallest useful hypothesis. Instrument only to tell hypotheses apart. Bound each investigation to a specific question.
- Never change things behind the user's back; tell them clearly instead.

## Operating model

The owner defines a bounded version and its acceptance criteria. A **PM** session writes the spec and starts a **Lead** as a separate session. The PM verifies the Lead's actual results against the criteria and escalates only owner decisions. The Lead owns judgment, architecture, integration, review, verification, and stopping when done or materially blocked. Do not automatically extend into adjacent work.

Clarify consequential scope, acceptance or safety questions before implementation; make routine reversible engineering choices autonomously.

**Model routing:** the Lead runs on the strongest model and owns judgment, task breakdown, integration and review. Use a mid-tier model as the default Worker for bounded implementation. Use the smallest model only for read-only search and mechanical edits whose result the Lead verifies. Escalate a Worker only when it has shown it can't handle the judgment. Diagnose a failure before paying for a bigger model.

**One code-writing session per checkout.** A session that runs alongside another uses its own worktree and integrates afterwards, because a shared build folder and uncommitted edits contaminate each other.

**Delegate** bounded work a Worker can do to the required quality; do it directly when coordination would cost more than it saves. Run Workers in parallel only for independent slices. Workers own one scoped task and do not spawn subagents.

**Brief Workers well:** goal, pointers to the relevant files and evidence, the known approach, invariants, constraints, acceptance criteria, what they may and may not touch, and when to stop.

While Workers run, do useful non-overlapping work or wait for their completion events. Do not poll or duplicate their investigation.

After two similar failures on a non-core blocker, reassess: isolate, change tools, delegate, defer, or stop with a precise blocker report.

**Report:** outcome, meaningful changes, net line delta, verification evidence and its limits, blockers, and the working-tree and publication state. Distinguish observed results from assumptions. Prefer deleting code to adding it.

## Documentation hygiene

Every decision is recorded and linked to its code, and every line in the decisions and code map earns its place:

- **Decisions are official.** An entry is written when the owner approves it, even mid-version, and changes only with the owner's approval. While the code doesn't match yet, "Since" says "<version> (in progress)". A replaced entry is removed and its ID listed under Retired IDs. IDs are never reused. Working notes go in the ledger or reports, never in the decisions.
- **Code map:** describes the code on the main branch. It is a factual map, not a decision, so it needs no owner approval, but it's updated only at a release's Record step, from the final code, for every subsystem the release touched.
- **Code tags:** the type or function that implements a decision carries a one-line comment ending with its ID, e.g. `(D-083)`. The reasoning lives in the decisions doc, not the comment. Searching for the ID finds all its code. A tag is never deferred to a later release.
- **Only verified content:** leave a field empty rather than guess.
- **When fixing a bug,** start from the subsystem in the code map, then follow its decision IDs, before changing anything.
- Do not create parallel planning documents; update existing sections rather than appending history.

## Working on the owner's machine

The owner uses this machine while agents work. Agent work must not take focus or cover the screen. Don't launch the app or bring windows to the front unless the task needs it and the owner has been told first. Never use, replace or quit the owner's own installed copy of the app. Test builds never touch the owner's real accounts, licenses or keychain items; an unexpected password prompt means stop and find the cause.

## Git hygiene

Commit on the current working branch; branch only when a change genuinely needs isolation. Keep commits focused and descriptive. Never amend, rebase or force-push shared history unless explicitly authorized.
