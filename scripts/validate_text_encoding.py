#!/usr/bin/env python3
"""Validate UTF-8 text files and common corruption markers."""

from __future__ import annotations

import argparse
from pathlib import Path


TEXT_SUFFIXES = {".md", ".txt", ".json", ".py", ".js", ".ps1", ".yml", ".yaml"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "output"}
BAD_MARKERS = ("\ufffd", "锟", "????")


def iter_files(paths: list[Path]) -> list[Path]:
    found: list[Path] = []
    for base in paths:
        if not base.exists():
            continue
        if base.is_file():
            if base.suffix.lower() in TEXT_SUFFIXES:
                found.append(base)
            continue
        for path in base.rglob("*"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                found.append(path)
    return sorted(set(found))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate UTF-8 text files and common corruption markers.")
    parser.add_argument("paths", nargs="+", help="Files or directories to scan.")
    args = parser.parse_args()

    self_path = Path(__file__).resolve()
    failures: list[str] = []
    for path in iter_files([Path(item) for item in args.paths]):
        if path.resolve() == self_path:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            failures.append(f"{path}: not valid UTF-8 ({exc})")
            continue
        for marker in BAD_MARKERS:
            if marker in text:
                failures.append(f"{path}: found suspicious marker {marker!r}")

    if failures:
        for item in failures:
            print(item)
        return 1

    print("Text encoding validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
