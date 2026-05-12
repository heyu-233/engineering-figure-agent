import os
import subprocess
import sys


def test_third_party_gemini_endpoint_fails_closed(tmp_path):
    key_file = tmp_path / "key.txt"
    key_file.write_text("fake-key", encoding="utf-8")
    env = {
        **os.environ,
        "NANOBANANA_BASE_URL": "https://relay.example.com",
        "NANOBANANA_API_KEY_FILE": str(key_file),
    }
    env.pop("NANOBANANA_ALLOW_THIRD_PARTY", None)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_image.py",
            "--timeout",
            "1",
            "A simple system architecture diagram.",
        ],
        text=True,
        capture_output=True,
        env=env,
    )

    assert result.returncode != 0
    assert "Refusing to send API keys" in result.stderr


def test_third_party_openai_endpoint_fails_closed(tmp_path):
    key_file = tmp_path / "key.txt"
    key_file.write_text("fake-key", encoding="utf-8")
    env = {
        **os.environ,
        "OPENAI_API_KEY_FILE": str(key_file),
    }
    env.pop("OPENAI_ALLOW_THIRD_PARTY", None)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_image.py",
            "--provider",
            "openai",
            "--openai-base-url",
            "https://relay.example.com/v1",
            "--timeout",
            "1",
            "A simple system architecture diagram.",
        ],
        text=True,
        capture_output=True,
        env=env,
    )

    assert result.returncode != 0
    assert "third-party OpenAI-compatible provider" in result.stderr


def test_highres_request_without_highres_model_fails_before_network(tmp_path):
    key_file = tmp_path / "key.txt"
    key_file.write_text("fake-key", encoding="utf-8")
    env = {
        **os.environ,
        "NANOBANANA_BASE_URL": "https://generativelanguage.googleapis.com",
        "NANOBANANA_API_KEY_FILE": str(key_file),
    }
    env.pop("NANOBANANA_HIGHRES_MODEL", None)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_image.py",
            "--highres",
            "A final-export system architecture diagram.",
        ],
        text=True,
        capture_output=True,
        env=env,
    )

    assert result.returncode != 0
    assert "NANOBANANA_HIGHRES_MODEL is not configured" in result.stderr


def test_openai_highres_request_without_highres_model_fails_before_network(tmp_path):
    key_file = tmp_path / "key.txt"
    key_file.write_text("fake-key", encoding="utf-8")
    env = {
        **os.environ,
        "OPENAI_API_KEY_FILE": str(key_file),
    }
    env.pop("OPENAI_IMAGE_HIGHRES_MODEL", None)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_image.py",
            "--provider",
            "openai",
            "--highres",
            "A final-export system architecture diagram.",
        ],
        text=True,
        capture_output=True,
        env=env,
    )

    assert result.returncode != 0
    assert "OPENAI_IMAGE_HIGHRES_MODEL is not configured" in result.stderr
