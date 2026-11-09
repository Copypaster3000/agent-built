# Code map

How the code works, per subsystem, for reading code and debugging. Rules and their reasons are in `DECISIONS.md` (cited by ID).

This is a factual map, not a decision, so it needs no owner approval. It describes the code on the main branch and is updated at each release's Record step, from the final code, for every subsystem the release touched. Every path and symbol must exist; leave a section empty rather than guess.

Each section uses one format, about 40 lines at most:
- **Does:** 1–2 lines.
- **Flow:** numbered steps naming the file and type or function.
- **Key files:** where to start reading.
- **Must hold:** invariants, with the decision ID when one governs.
- **Debug from:** a user-visible message or error code → where to start looking.

## <Subsystem, e.g. Saving>
**Does:** Saves the user's draft to disk and backs it up before every overwrite.
**Flow:**
1. `src/editor/Editor.ts` `save()` hands the draft to `src/storage/write.ts` `writeWithBackup`.
2. `createBackup` (`src/storage/backup.ts`) copies the current file to `backups/` with a timestamp; a failure stops the write (D-001).
3. `writeWithBackup` writes to a temporary file, then renames it over the original.
**Key files:**
- `src/storage/write.ts`: every write goes through here.
- `src/storage/backup.ts`: backups and restore.
**Must hold:**
- No write starts before its backup succeeds (D-001).
- Writes are atomic: temporary file, then rename.
**Debug from:**
- "Couldn't save your work" → `writeWithBackup` error path; check the backup step first.
