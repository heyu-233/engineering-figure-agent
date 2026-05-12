#!/usr/bin/env python3
"""Check local Markdown links and image paths."""

from __future__ import annotations

import re
import sys
from pathlib import Path


LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")


def is_external(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:", "#"))


def normalize_target(target: str) -> str:
    target = target.split("#", 1)[0].strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return target


def main() -> int:
    root = Path(".").resolve()
    files = [Path("README.md"), Path("README.en.md"), Path("README.zh-CN.md")]
    files.extend(Path("docs").rglob("*.md"))
    files.extend(Path("adapters").rglob("*.md") if Path("adapters").exists() else [])

    missing: list[str] = []
    for file in files:
        if not file.is_file():
            continue
        text = file.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = normalize_target(raw)
            if not target or is_external(target):
                continue
            resolved = (file.parent / target).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                missing.append(f"{file}: link escapes repo: {raw}")
                continue
            if not resolved.exists():
                missing.append(f"{file}: missing {raw}")

    if missing:
        print("\n".join(missing), file=sys.stderr)
        return 1
    print("Markdown link check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
