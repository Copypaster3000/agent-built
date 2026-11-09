# Decisions

> **Example.** A filled-in version of `templates/DECISIONS.md` for a made-up app, to show the format. Start from the template, not this file.

The owner-approved product and engineering decisions, grouped by area. This is an official document: an entry is written when the owner approves the decision and changes only with the owner's approval. A replaced decision is removed (git history keeps it) and its ID listed once under "Retired IDs". IDs are permanent and never reused or renumbered; code, the ledger and other docs refer to them.

Entry format, exactly:

```
### D-001: <the rule, as a short imperative or fact>
- **Rule:** what is true or required now. 1–4 lines. Plain words; the specifics that matter (numbers, names, exact messages).
- **Why:** the reason in 1–2 lines; the owner's own words in quotes when they decided it.
- **Code:** `path/to/file.ext` `TypeOrFunction`. Every place that implements it. "None (process)" for process-only rules.
- **Since:** version or date; "<version> (in progress)" while the code doesn't match yet. Replaces D-0xx (if any).
```

Rules for writing entries:
- One decision per entry. If two rules can change independently, they are two entries.
- No history, narratives, working notes, open questions or alternatives considered. Evidence goes in the ledger or reports; history in git.
- Update an entry in place when the rule changes (and its Since line); don't append "update" paragraphs.
- Every implementing place carries a one-line code comment ending with the ID, e.g. `// Saves before every write (D-002).` Searching for the ID finds the rule and all its code.

## <Area, e.g. Data and storage>

### D-001: Every write is backed up first
- **Rule:** Before any change to the user's data, the app saves a copy the user can restore from in one click. If the backup fails, the write doesn't start.
- **Why:** Owner: "never risk someone's data to save a second."
- **Code:** `src/storage/backup.ts` `createBackup`; `src/storage/write.ts` `writeWithBackup`.
- **Since:** 1.0.0.

## <Area, e.g. Messages>

### D-002: Error titles state the reason
- **Rule:** A popup that isn't a real failure is titled with its reason in a few words ("Nothing to save yet"); real failures keep "Couldn't save your work".
- **Why:** Owner: "the reason should be the header."
- **Code:**
- **Since:** 1.2.0 (in progress).

## Retired IDs

None yet. When a decision is replaced, remove it above and list it here, e.g. `- D-007: replaced by D-012.`
