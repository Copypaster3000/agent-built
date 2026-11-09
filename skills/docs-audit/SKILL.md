---
name: docs-audit
description: Audit docs/DECISIONS.md and docs/CODE_MAP.md against the code at a release's Record step, before the owner approves the release, or whenever the owner asks. Includes the mechanical checker the Lead also runs before handing in Record.
---

# Docs audit

Makes `docs/DECISIONS.md` and `docs/CODE_MAP.md` exactly match the code, so the owner approves a release on accurate docs. Rules: `CLAUDE.md` "Documentation hygiene" and `docs/RELEASE_PROCESS.md`, Record step.

## 1. Mechanical check (the Lead runs this too)

```bash
python3 .claude/skills/docs-audit/check_docs.py
```

It checks every repo path and code name cited in both docs, decision ID bookkeeping (no duplicates or unexplained gaps; retired and reserved IDs listed), that every code `(D-###)` tag names an active decision, and the ledger's "next free IDs" line. Set your folders and ID prefix in its CONFIG block first.

Any FAIL is fixed before going further. WARN lines are judged: a name cited beside the wrong file gets the right file; an untagged decision gets a tag if code implements it; an "(in progress)" entry must not belong to the version being released.

The Lead runs it before handing in Record and fixes its own misses. The PM runs it again on the release commit.

## 2. Line-by-line review (PM)

Run it on the **final** release candidate's commit. Any code change after an earlier audit means auditing again.

Scope: every line of both docs that changed since the previous release tag, and every code file that changed.

```bash
git diff <previous-release-tag>..HEAD -- docs/DECISIONS.md docs/CODE_MAP.md
git diff --stat <previous-release-tag>..HEAD -- <your source folders>
```

**Coverage first:** for each changed code file, name its `CODE_MAP.md` subsystem and the decisions it implements, then confirm that section (Flow, Must hold, Debug from) and those decisions changed to match, or note why no doc change is needed. The checker can't see missing content, so a clean checker is never the whole audit.

For each changed decision:
- the Rule matches what the code does (cite file:line); quoted messages match the code exactly;
- Code names every implementing place, and that code carries the tag;
- Since is this version; no "(in progress)" left for it; replaced IDs are under Retired IDs;
- nothing remains from a direction that was dropped during the version;
- no working notes, history, evidence or open questions; nothing repeated from another entry.

For each changed code-map section: Flow steps match the code, Must hold lines are true, Debug from points at real messages or error codes.

Every line must earn its place: delete what an agent wouldn't need.

**Glossary:** check `docs/GLOSSARY.md` against what the owner said during the version (terms added, renamed or used differently). Bring any needed change to the owner first; edit the glossary only after they approve.

## 3. Report to the owner

Clear and very concise; the depth stays with the PM. List only:
- what changed in the docs this release, one line per decision or code-map section;
- any glossary term to add or correct, with the proposed wording, for approval;
- anything needing the owner: a rule the code doesn't match, or an "(in progress)" entry that isn't shipping. One line each, with the choice: change the decision, finish the code, or remove the entry and return the item to the ledger.

Say "audit clean" when nothing needs the owner.

Decisions change only with the owner's approval. Mechanical corrections (a moved file, a renamed function, a missing tag) don't need it, but list them.
