#!/usr/bin/env python3
"""Validate the pruned runtime skill package and its token budget."""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from sync_codex_skill import ALLOW, sync


TEXT_SUFFIXES = {".md", ".txt", ".json", ".py", ".js", ".ps1", ".yml", ".yaml"}
FORBIDDEN_TOP_LEVEL = {
    ".github",
    "adapters",
    "docs",
    "examples",
    "tests",
    "README.md",
    "README.en.md",
    "README.zh-CN.md",
    "providers.md",
    "requirements.txt",
}


def iter_text_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES)


def count_tokens(root: Path) -> tuple[int, list[tuple[int, str]]]:
    import tiktoken

    encoder = tiktoken.get_encoding("o200k_base")
    rows: list[tuple[int, str]] = []
    total = 0
    for path in iter_text_files(root):
        tokens = len(encoder.encode(path.read_text(encoding="utf-8")))
        rel = path.relative_to(root).as_posix()
        rows.append((tokens, rel))
        total += tokens
    rows.sort(reverse=True)
    return total, rows


def validate_structure(root: Path) -> None:
    names = {path.name for path in root.iterdir()}
    expected = set(ALLOW)
    if names != expected:
        missing = sorted(expected - names)
        extra = sorted(names - expected)
        raise SystemExit(f"Runtime package mismatch. Missing: {missing} Extra: {extra}")

    present_forbidden = sorted(name for name in FORBIDDEN_TOP_LEVEL if (root / name).exists())
    if present_forbidden:
        raise SystemExit(f"Runtime package contains forbidden top-level entries: {present_forbidden}")

    skill_files = sorted(path.relative_to(root).as_posix() for path in root.rglob("SKILL.md"))
    if skill_files != ["SKILL.md"]:
        raise SystemExit(f"Expected exactly one runtime SKILL.md at root, found: {skill_files}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the synced runtime package and token budget.")
    parser.add_argument(
        "--token-budget",
        type=int,
        default=38000,
        help="Maximum allowed total runtime tokens using tiktoken o200k_base.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    with tempfile.TemporaryDirectory(prefix="efa-runtime-") as tmp:
        target = Path(tmp) / "engineering-figure-agent"
        sync(target)
        validate_structure(target)
        total, rows = count_tokens(target)

    print(f"Runtime token total: {total}")
    print("Top runtime files:")
    for tokens, rel in rows[:8]:
        print(f"  {tokens:5d}  {rel}")

    if total > args.token_budget:
        raise SystemExit(f"Runtime token budget exceeded: {total} > {args.token_budget}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
