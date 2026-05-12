import subprocess
import sys


def test_prompt_builder_selects_chinese_template_for_chinese_background():
    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_engineering_figure_prompt.py",
            "--figure-template",
            "system-architecture",
            "一个包含 OCR、向量检索和答案生成的 RAG 系统。",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "技术背景" in result.stdout
    assert "RAG" in result.stdout


def test_generate_image_print_prompt_does_not_require_api_key():
    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_image.py",
            "--figure-template",
            "algorithm-workflow",
            "--print-prompt",
            "A training pipeline with data cleaning, model fitting, validation, and deployment.",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "Technical Background" in result.stdout
    assert "training pipeline" in result.stdout
