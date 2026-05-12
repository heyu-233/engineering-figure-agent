#!/usr/bin/env python3
"""Unified convenience CLI for Engineering Figure Agent."""

from __future__ import annotations

import argparse
import compileall
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def run_command(args: list[str]) -> int:
    return subprocess.call(args, cwd=ROOT)


def cmd_prompt(args: argparse.Namespace) -> int:
    if bool(args.figure_template) == bool(args.materials_figure):
        print("Choose exactly one of --figure-template or --materials-figure.", file=sys.stderr)
        return 2
    if args.materials_figure:
        command = [
            sys.executable,
            str(SCRIPTS / "build_materials_figure_prompt.py"),
            "--materials-figure",
            args.materials_figure,
        ]
    else:
        command = [
            sys.executable,
            str(SCRIPTS / "build_engineering_figure_prompt.py"),
            "--figure-template",
            args.figure_template,
        ]
    if args.lang:
        command.extend(["--lang", args.lang])
    if args.style_note:
        command.extend(["--style-note", args.style_note])
    if args.background_file:
        command.extend(["--background-file", args.background_file])
    if args.background:
        command.append(args.background)
    return run_command(command)


def cmd_image(args: argparse.Namespace) -> int:
    return run_command([sys.executable, str(SCRIPTS / "generate_image.py"), *args.args])


def cmd_plot(args: argparse.Namespace) -> int:
    spec_out = Path(args.spec_out)
    if not spec_out.is_absolute():
        spec_out = ROOT / spec_out
    spec_out.parent.mkdir(parents=True, exist_ok=True)

    build_code = run_command(
        [
            sys.executable,
            str(SCRIPTS / "build_plot_spec.py"),
            args.request_file,
            "--out",
            str(spec_out),
        ]
    )
    if build_code != 0:
        return build_code

    return run_command(
        [
            sys.executable,
            str(SCRIPTS / "plot_publication_figure.py"),
            str(spec_out),
            "--out-path",
            args.out_path,
            "--formats",
            *args.formats,
        ]
    )


def cmd_check(_: argparse.Namespace) -> int:
    ok = compileall.compile_dir(str(SCRIPTS), quiet=1)
    if not ok:
        return 1
    prompt_code = run_command(
        [
            sys.executable,
            str(SCRIPTS / "generate_image.py"),
            "--figure-template",
            "system-architecture",
            "--print-prompt",
            "A retrieval system with OCR, embedding, vector search, reranking, and answer synthesis.",
        ]
    )
    return prompt_code


def cmd_wizard(_: argparse.Namespace) -> int:
    wizard = SCRIPTS / "wizard.ps1"
    if sys.platform.startswith("win"):
        return run_command(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(wizard)])
    print(f"PowerShell wizard is available at: {wizard}")
    print("Use `efa prompt`, `efa image`, or `efa plot` for portable workflows.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Engineering Figure Agent unified CLI.")
    sub = parser.add_subparsers(dest="command", required=True)

    prompt = sub.add_parser("prompt", help="Build an engineering figure prompt without network calls.")
    prompt.add_argument("background", nargs="?", help="Technical background text.")
    prompt.add_argument("--background-file", help="Read technical background from a file.")
    prompt.add_argument("--figure-template")
    prompt.add_argument("--materials-figure")
    prompt.add_argument("--lang", choices=("en", "zh"))
    prompt.add_argument("--style-note")
    prompt.set_defaults(func=cmd_prompt)

    image = sub.add_parser("image", help="Forward arguments to generate_image.py.")
    image.add_argument("args", nargs=argparse.REMAINDER)
    image.set_defaults(func=cmd_image)

    plot = sub.add_parser("plot", help="Build a plot spec and render it.")
    plot.add_argument("request_file")
    plot.add_argument("--spec-out", default="output/plot-spec.json")
    plot.add_argument("--out-path", default="output/publication-figure")
    plot.add_argument("--formats", nargs="+", default=["png", "pdf", "svg"])
    plot.set_defaults(func=cmd_plot)

    check = sub.add_parser("check", help="Run offline smoke checks.")
    check.set_defaults(func=cmd_check)

    wizard = sub.add_parser("wizard", help="Launch the PowerShell wizard when available.")
    wizard.set_defaults(func=cmd_wizard)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
