# Glossary

The shared words for this project. Agents, docs, code comments, reports and user-facing text all use these terms, so everyone means the same thing.

Rules:
- One line per term: what it means to the user, then the code name if it differs.
- A term is added or changed only with the owner's approval. At each release, the PM checks this file against what the owner said during the version and brings any needed change to the owner first.
- When a decision governs a term, cite its ID.

## <The product's own concepts>

- **Draft:** the user's edited version, not yet saved to the real thing. Code: `pendingState`.
- **Restore:** putting back a saved backup in one step (D-001).
- **Sync:** pulling the latest data from the user's account. Never called "refresh" in user-facing text.

## <Process terms>

- **Owner:** the person who approves scope, behavior, fixes and releases.
- **PM:** the agent session that runs the release process for the owner.
- **Lead:** the agent session that implements one version.
- **Finding:** a possible problem raised by a review, audit or test, before it passes the finding gate.
