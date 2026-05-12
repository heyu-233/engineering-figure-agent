import subprocess
import sys


def test_efa_prompt_smoke():
    result = subprocess.run(
        [
            sys.executable,
            "scripts/efa.py",
            "prompt",
            "--figure-template",
            "system-architecture",
            "--lang",
            "en",
            "A RAG pipeline with OCR, embedding, vector search, and answer synthesis.",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "Technical Background" in result.stdout


def test_efa_materials_prompt_smoke():
    result = subprocess.run(
        [
            sys.executable,
            "scripts/efa.py",
            "prompt",
            "--materials-figure",
            "device-architecture",
            "--lang",
            "en",
            "A layered battery device with a stabilized electrolyte interface.",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "materials-science device architecture figure" in result.stdout


def test_efa_check_smoke():
    subprocess.run(
        [sys.executable, "scripts/efa.py", "check"],
        check=True,
        text=True,
        capture_output=True,
    )
