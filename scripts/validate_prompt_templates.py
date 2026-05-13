#!/usr/bin/env python3
"""Validate Chinese prompt templates and catch likely mojibake regressions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ENGINEERING_EXPECTATIONS = {
    "graphical-abstract": ["创建工程或 AI 论文用的 graphical abstract", "技术背景：", "{background}"],
    "system-architecture": ["系统架构图", "技术背景：", "{background}"],
    "algorithm-workflow": ["算法流程图", "技术背景：", "{background}"],
    "electronic-schematic": ["嵌入式系统", "技术背景：", "{background}"],
}

MATERIALS_EXPECTATIONS = {
    "graphical-abstract": ["材料科学论文", "graphical abstract", "Scientific Background:", "{background}"],
    "mechanism-figure": ["材料科学论文", "机理示意图", "Scientific Background:", "{background}"],
    "device-architecture": ["材料科学论文", "器件结构图", "Scientific Background:", "{background}"],
    "processing-workflow": ["材料科学论文", "加工流程图", "Scientific Background:", "{background}"],
}

SUSPICIOUS_MOJIBAKE_FRAGMENTS = [
    "鍒涘缓",
    "鎶€鏈",
    "鐧借壊",
    "鏈熷垔",
    "鑳屾櫙",
    "缁撴瀯",
    "绯荤粺",
    "鏁版嵁",
]


def cjk_count(text: str) -> int:
    return sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")


def validate_prompt_text(label: str, text: str, required_fragments: list[str], failures: list[str]) -> None:
    if cjk_count(text) < 20:
        failures.append(f"{label}: expected meaningful Chinese content, but too few CJK characters were found")
    for fragment in required_fragments:
        if fragment not in text:
            failures.append(f"{label}: missing required fragment {fragment!r}")

    hits = [fragment for fragment in SUSPICIOUS_MOJIBAKE_FRAGMENTS if fragment in text]
    if hits:
        failures.append(f"{label}: found suspicious mojibake fragments {hits}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_template_file(path: Path, expectations: dict[str, list[str]], failures: list[str]) -> None:
    data = load_json(path)
    actual_keys = set(data.keys())
    expected_keys = set(expectations.keys())
    if actual_keys != expected_keys:
        failures.append(f"{path}: template keys mismatch. expected={sorted(expected_keys)} actual={sorted(actual_keys)}")
        return

    for key, required in expectations.items():
        entry = data.get(key, {})
        if "en" not in entry or "zh" not in entry:
            failures.append(f"{path}:{key}: each template must provide both 'en' and 'zh'")
            continue
        validate_prompt_text(f"{path}:{key}:zh", entry["zh"], required, failures)


def validate_figure_brief(path: Path, failures: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    required = ["图的目标", "论文主张", "图类型", "面板规划", "风格约束"]
    validate_prompt_text(str(path), text, required, failures)


def validate_prompt_builder_test(path: Path, failures: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    required = ["一个包含 OCR、向量检索和答案生成的 RAG 系统。", 'assert "技术背景" in result.stdout']
    for fragment in required:
        if fragment not in text:
            failures.append(f"{path}: missing expected test fragment {fragment!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Chinese prompt templates and catch likely mojibake.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    failures: list[str] = []

    validate_template_file(root / "assets" / "prompt-templates" / "engineering-figure-templates.json", ENGINEERING_EXPECTATIONS, failures)
    validate_template_file(root / "assets" / "prompt-templates" / "materials-science-figure-templates.json", MATERIALS_EXPECTATIONS, failures)
    validate_figure_brief(root / "templates" / "figure-brief" / "figure-brief.zh-CN.md", failures)
    validate_prompt_builder_test(root / "tests" / "test_prompt_builder.py", failures)

    if failures:
        for item in failures:
            print(item, file=sys.stderr)
        return 1

    print("Prompt template validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
