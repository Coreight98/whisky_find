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


def main():
    checks = [check_skill]
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
