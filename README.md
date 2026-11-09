# agent-built

How I build and ship software with AI agents while keeping every decision my own.

AI agents can write most of the code, but they forget everything between sessions, and they'll happily build on top of a decision you made last month without knowing it exists. This repo is the process and the docs I use as a solo developer to keep agents productive and keep myself in charge: what gets built, how it works, and what ships. Everything here is general, meant to be adapted to your own projects.

It comes from building [Thumbwise](https://thumbwise.app), a Mac app shipped this way.

**To use it:** put `templates/CLAUDE.md` in your project root, copy the other templates into `docs/`, and copy `process/release-process.md` to `docs/RELEASE_PROCESS.md`.

---

## Release process

[`process/release-process.md`](process/release-process.md)

**What:** the steps every version goes through: scope, build, independent review, the finding gate, triage, fix rounds, a real-world test, a docs audit and release, with a gate at each step and clear rules for when to stop.

**Why:** agents are fast but overconfident. This puts every finding through a second agent that tries to disprove it, brings me only real decisions in one batch, and stops reviews from widening the scope forever.

![How I ship with AI agents](images/release-process.png)

## CLAUDE.md

[`templates/CLAUDE.md`](templates/CLAUDE.md)

**What:** the instructions file every agent reads first: the sources of truth and their order, evidence rules, engineering principles, who does what (PM, Lead, Workers), which model to use for what, and how to brief a Worker. Using a tool other than Claude Code? Rename it `AGENTS.md`.

**Why:** every agent session starts from zero. This gives each one the same rules and habits in the first minute, so you're not re-explaining how you work every time.

## DECISIONS.md

[`templates/DECISIONS.md`](templates/DECISIONS.md)

**What:** every rule you've approved, each with an ID, the reason in your own words, and the exact code that implements it. That code carries the ID in a one-line comment, so one search finds the rule, its reason and all its code.

**Why:** it's the project's memory. New ideas are checked against it before they're built, so no agent quietly undoes or contradicts a past decision, and six months from now you still know *why* something works the way it does.

![How my docs never drift from the code](images/docs-sync.png)

## CODE_MAP.md

[`templates/CODE_MAP.md`](templates/CODE_MAP.md)

**What:** how the code works, one section per subsystem: what it does, the flow step by step, key files, what must always hold, and where to start debugging from a given error.

**Why:** a new agent session is up to speed in minutes instead of rediscovering the codebase. It's updated from the final code at every release and audited line by line, so it can't go stale.

## GLOSSARY.md

[`templates/GLOSSARY.md`](templates/GLOSSARY.md)

**What:** the shared words for your product and process, one line each, with the code name when it differs.

**Why:** when you, your agents, your docs and your user-facing text all use the same words, instructions aren't misread and users see consistent language.

## LEDGER.md

[`templates/LEDGER.md`](templates/LEDGER.md)

**What:** the open list of fixes and the current version's scope. Every item has an ID and a "done means" line, and it leaves only when it's fixed in a released version or you drop it.

**Why:** nothing found in a review or test gets lost, and nothing sneaks into a release unplanned. Ideas go to a separate backlog, so the ledger stays a list of things that must be done.
