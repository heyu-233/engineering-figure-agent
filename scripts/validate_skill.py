#!/usr/bin/env python3
"""Small local validation for the Codex skill package."""

from __future__ import annotations

import re
import sys
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    skill = root / "SKILL.md"
    if not skill.is_file():
        print("Missing SKILL.md", file=sys.stderr)
        return 1
    text = skill.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        print("SKILL.md must start with YAML frontmatter", file=sys.stderr)
        return 1
    frontmatter = match.group(1)
    if "name:" not in frontmatter:
        print("SKILL.md frontmatter missing name", file=sys.stderr)
        return 1
    if "description:" not in frontmatter:
        print("SKILL.md frontmatter missing description", file=sys.stderr)
        return 1
    if not (root / "agents" / "openai.yaml").is_file():
        print("Missing agents/openai.yaml", file=sys.stderr)
        return 1
    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
