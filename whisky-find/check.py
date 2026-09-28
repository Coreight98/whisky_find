#!/usr/bin/env python3
"""Structural checks for the whisky-find skill.

Run: python3 whisky-find/check.py
Checks only what a machine can check: frontmatter, required sections, and the
shape of the source tables. Whether a research card is any good is checked by
running references/evals.md by hand.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SKILL = ROOT / "SKILL.md"

REQUIRED_SECTIONS = [
    "## Identify the bottle",
    "## Language routing",
    "## lookup",
    "## siblings",
    "## Trust rules",
]


def split_frontmatter(path):
    """Return (frontmatter dict, body). Raises AssertionError if malformed."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match, f"{path.name}: missing YAML frontmatter"
    fields = dict(re.findall(r"^([a-z_]+):\s*(.+)$", match.group(1), re.M))
    return fields, text[match.end():]


def check_skill():
    fields, body = split_frontmatter(SKILL)
    assert fields.get("name") == "whisky-find", \
        f"SKILL.md: name must be 'whisky-find', got {fields.get('name')!r}"
    description = fields.get("description", "")
    assert len(description) >= 40, \
        "SKILL.md: description must be substantial enough to trigger on"
    for section in REQUIRED_SECTIONS:
        assert section in body, f"SKILL.md: missing section {section!r}"


SOURCES = ROOT / "references" / "sources.md"

KNOWN_LANGS = {"en", "ja", "zh", "fr", "de", "it", "nl", "ko"}


def parse_table(body, heading):
    """Return the rows of the first markdown table under `heading`.

    Each row is a list of stripped cell strings. The header row and the
    `|---|` separator are skipped.
    """
    start = body.index(heading)
    after = body[start + len(heading):]
    rows = []
    for line in after.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(set(c) <= {"-", ":"} and c for c in cells):
            continue
        rows.append(cells)
    assert rows, f"no table found under {heading!r}"
    return rows[1:]


def check_sources():
    body = SOURCES.read_text(encoding="utf-8")
    heading = "## Bottler and producer languages"
    assert heading in body, f"sources.md: missing section {heading!r}"
    rows = parse_table(body, heading)
    assert len(rows) >= 20, \
        f"sources.md: bottler table has only {len(rows)} rows; it is the whole point of the file"
    for row in rows:
        assert len(row) >= 2, f"sources.md: malformed row {row!r}"
        name, lang = row[0], row[1]
        assert name, f"sources.md: row with empty name: {row!r}"
        assert lang in KNOWN_LANGS, \
            f"sources.md: {name!r} has language {lang!r}, not in {sorted(KNOWN_LANGS)}"


def main():
    checks = [check_skill, check_sources]
    failures = []
    for check in checks:
        try:
            check()
        except AssertionError as exc:
            failures.append(str(exc))
    for failure in failures:
        print(f"FAIL: {failure}")
    if failures:
        return 1
    print(f"ok: {len(checks)} check(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
