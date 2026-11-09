#!/usr/bin/env python3
"""Mechanical checks for docs/DECISIONS.md and docs/CODE_MAP.md. Read-only.

Run from anywhere inside your repo:  python3 .claude/skills/docs-audit/check_docs.py
Exit 1 on any FAIL. WARN lines are for a person to judge. It checks existence and ID
bookkeeping only; whether a rule matches what the code does is the reviewer's job.

What it checks:
  - every repo path and code name cited in backticks in both docs exists;
  - decision IDs: no duplicates, no unexplained gaps, retired and reserved IDs listed;
  - every D-### tag in the code points at an active decision;
  - the ledger's "next free IDs" line is right;
  - warns about active decisions with no code tag and "(in progress)" entries.

Adjust the CONFIG block to your project's layout.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

# ---- CONFIG -------------------------------------------------------------
DECISIONS_DOC = "docs/DECISIONS.md"
CODE_MAP_DOC = "docs/CODE_MAP.md"
LEDGER_DOC = "docs/LEDGER.md"
# Folders that hold your code; code names and D-### tags are searched here.
SOURCE_DIRS = ("src", "lib", "scripts")
# Extra folders that may be cited as paths (tests, config, docs...).
OTHER_DIRS = ("tests", "config", "docs", ".claude")
# Single files at the repo root that may be cited (e.g. package.json).
ROOT_FILES = ("package.json", "pyproject.toml", "Package.swift", "Cargo.toml", "go.mod")
# File extensions a bare file name may have when cited without a folder.
EXTENSIONS = "swift|py|ts|tsx|js|jsx|go|rs|rb|java|kt|cs|cpp|c|h|m|sh|json|yaml|yml|toml|md|plist"
# The ID prefix your ledger uses for fixes, as in "next free are **F-004** and **D-003**".
FIX_PREFIX = "F"
# -------------------------------------------------------------------------

REPO = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                           text=True).stdout.strip() or ".").resolve()
DECISIONS, CODE_MAP, LEDGER = REPO / DECISIONS_DOC, REPO / CODE_MAP_DOC, REPO / LEDGER_DOC
REPO_PREFIXES = tuple(f"{d}/" for d in SOURCE_DIRS + OTHER_DIRS) + ROOT_FILES
fails, warns = [], []


def files_under(*dirs):
    out = []
    for d in dirs:
        for root, subdirs, names in os.walk(REPO / d):
            subdirs[:] = [s for s in subdirs if not s.startswith(".") or s == ".claude"]
            out += [Path(root) / n for n in names if not n.startswith(".")]
    return out


SOURCES = files_under(*SOURCE_DIRS)
ALL_FILES = files_under(*SOURCE_DIRS, *OTHER_DIRS)
TEXT = {}


def text(path):
    if path not in TEXT:
        TEXT[path] = path.read_text(errors="ignore")
    return TEXT[path]


def resolve(token):
    """Repo-relative path, or a bare file name found once in the repo; None if not a path."""
    if token.startswith(REPO_PREFIXES) and " " not in token:
        target = REPO / token.rstrip("/")
        if not target.exists():
            return []
        return [target] if target.is_file() else files_under(token.rstrip("/"))
    if re.fullmatch(rf"[\w.-]+\.({EXTENSIONS})", token):
        root = REPO / token
        return [root] if root.is_file() else [f for f in ALL_FILES if f.name == token]
    return None


def symbols(token):
    token = re.sub(r"\(.*\)$", "", token)
    return [s for s in re.split(r"[.\s:]", token) if re.fullmatch(r"[A-Za-z_]\w*", s)]


def check_paths_and_symbols():
    paths = names = 0
    for doc in (DECISIONS, CODE_MAP):
        lines = text(doc).splitlines()
        start = next((i for i, l in enumerate(lines) if l.startswith("## ")), 0)  # skip the format header
        for n, line in enumerate(lines[start:], start + 1):
            for clause in line.split(";"):
                files = None
                for token in re.findall(r"`([^`]+)`", clause):
                    found = resolve(token)
                    if found is not None:
                        paths += 1
                        files = found or None
                        # A bare name the code creates at runtime is not a missing file.
                        if not found and not ("/" not in token and any(f'"{token}"' in text(f) for f in SOURCES)):
                            fails.append(f"FAIL path missing: {doc.name}:{n} `{token}`")
                        continue
                    if re.search(r"[\s=<>{}…,\"'/]", token) and not re.fullmatch(r"[\w.]+\(.*\)", token):
                        continue  # messages, values and runtime paths are not code names
                    for name in symbols(token):
                        names += 1
                        if files and any(name in text(f) for f in files):
                            continue
                        if any(name in text(f) for f in SOURCES):
                            if files:
                                warns.append(f"WARN {doc.name}:{n} `{token}`: {name} is not in the file cited before it")
                            continue
                        fails.append(f"FAIL name missing: {doc.name}:{n} `{token}` ({name})")
    print(f"Checked {paths} paths and {names} code names.")


def check_ids():
    doc = text(DECISIONS)
    doc = doc[doc.index("\n## "):] if "\n## " in doc else doc  # skip the format example in the header
    active = re.findall(r"^### D-(\d{3}):", doc, re.M)
    retired_block = doc.split("## Retired IDs", 1)[1] if "## Retired IDs" in doc else ""
    retired = re.findall(r"^- D-(\d{3})\b", retired_block, re.M)
    ledger = text(LEDGER) if LEDGER.exists() else ""
    reserved = re.findall(r"D-(\d{3}) is reserved", ledger)
    for i in sorted({x for x in active if active.count(x) > 1}):
        fails.append(f"FAIL duplicate active ID D-{i}")
    for i in sorted(set(active) & set(retired)):
        fails.append(f"FAIL D-{i} is both active and retired")
    used = {int(x) for x in active + retired + reserved}
    for i in range(1, max(used, default=0) + 1):
        if i not in used:
            fails.append(f"FAIL D-{i:03d} is neither active, retired nor reserved")
    m = re.search(rf"next free are \*\*{FIX_PREFIX}-(\d+)\*\* and \*\*D-(\d+)\*\*", ledger)
    if not m:
        warns.append("WARN ledger has no 'next free' IDs line")
    else:
        if int(m.group(2)) != max(used, default=0) + 1:
            fails.append(f"FAIL ledger says next decision is D-{m.group(2)}, highest used is D-{max(used, default=0):03d}")
        log = subprocess.run(["git", "log", "--all", "--format=%s%n%b"], cwd=REPO,
                             capture_output=True, text=True).stdout
        seen = [int(x) for x in re.findall(rf"\b{FIX_PREFIX}-(\d+)", log + ledger.replace(m.group(0), ""))]
        if seen and int(m.group(1)) <= max(seen):
            fails.append(f"FAIL ledger says next fix ID is {FIX_PREFIX}-{m.group(1)}, "
                         f"but {FIX_PREFIX}-{max(seen):03d} is already used")
    # Code tags must point at active decisions.
    tagged = {}
    for f in files_under(*SOURCE_DIRS, *(d for d in OTHER_DIRS if d.startswith("test"))):
        for tag in re.findall(r"\bD-(\d{3})\b", text(f)):
            tagged.setdefault(tag, set()).add(f)
    for tag in sorted(tagged):
        if tag not in active:
            where = sorted(str(p.relative_to(REPO)) for p in tagged[tag])[:3]
            fails.append(f"FAIL code mentions D-{tag}, which is not an active decision: {where}")
    untagged = [f"D-{i}" for i in active if i not in tagged and not re.search(
        rf"### D-{i}:.*?\n- \*\*Code:\*\* None", doc, re.S | re.M)]
    if untagged:
        warns.append(f"WARN active decisions with no code tag: {', '.join(untagged)}")
    for d, since in re.findall(r"### (D-\d{3}):[^\n]*\n(?:- [^\n]*\n){0,4}- \*\*Since:\*\* ([^\n]*\(in progress\))", doc):
        warns.append(f"WARN {d} is {since}")
    print(f"{len(active)} active, {len(retired)} retired, {len(reserved)} reserved decision IDs.")


for required in (DECISIONS, CODE_MAP):
    if not required.exists():
        sys.exit(f"Missing {required.relative_to(REPO)}; adjust the CONFIG block.")
check_paths_and_symbols()
check_ids()
for line in fails + warns:
    print(line)
print("RESULT:", "FAIL" if fails else "PASS", f"({len(fails)} fail, {len(warns)} warn)")
sys.exit(1 if fails else 0)
