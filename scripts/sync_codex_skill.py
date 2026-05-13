#!/usr/bin/env python3
"""Sync a pruned runtime Codex skill install."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = Path.home() / ".codex" / "skills" / "engineering-figure-agent"
ALLOW = [
    "SKILL.md",
    "agents",
    "assets",
    "references",
    "scripts",
    "templates",
    "schemas",
    "secrets",
    "LICENSE",
]
RUNTIME_SCRIPT_ALLOW = {
    "build_engineering_figure_prompt.py",
    "build_materials_figure_prompt.py",
    "build_plot_spec.py",
    "check_setup.ps1",
    "efa.py",
    "generate_image.js",
    "generate_image.py",
    "load_nanobanana_env.ps1",
    "plot_publication_figure.py",
    "wizard.ps1",
}


def safe_target(path: Path) -> Path:
    resolved = path.resolve()
    if resolved.name != "engineering-figure-agent":
        raise SystemExit(f"Refusing to sync to unexpected folder: {resolved}")
    if resolved == ROOT:
        raise SystemExit("Refusing to sync into the source repository itself.")
    return resolved


def remove_contents(path: Path) -> None:
    if not path.exists():
        return
    for item in path.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def copy_item(source: Path, target: Path) -> None:
    if not source.exists():
        return
    if source.is_dir() and source.name == "scripts":
        target.mkdir(parents=True, exist_ok=True)
        for child in source.iterdir():
            if child.name in RUNTIME_SCRIPT_ALLOW:
                copy_item(child, target / child.name)
        return
    if source.is_dir():
        ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache")
        shutil.copytree(source, target, ignore=ignore)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def sync(target: Path) -> None:
    target = safe_target(target)
    target.mkdir(parents=True, exist_ok=True)
    remove_contents(target)
    for name in ALLOW:
        copy_item(ROOT / name, target / name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync a pruned runtime Codex skill install.")
    parser.add_argument("--target", type=Path, default=Path(os.getenv("CODEX_SKILL_TARGET", DEFAULT_TARGET)))
    args = parser.parse_args()
    sync(args.target)
    print(f"Synced runtime skill to {args.target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
