import json
import re
import subprocess
import sys
from pathlib import Path


def _extract_json_block(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"```json\s*(.*?)\s*```", text, re.S)
    assert match, f"No JSON block found in {path}"
    return json.loads(match.group(1))


def test_benchmark_request_builds_and_renders(tmp_path):
    request = _extract_json_block(Path("examples/figure-briefs/benchmark-plot-request.md"))
    request_path = tmp_path / "request.json"
    spec_path = tmp_path / "spec.json"
    out_prefix = tmp_path / "benchmark"
    request_path.write_text(json.dumps(request), encoding="utf-8")

    subprocess.run(
        [sys.executable, "scripts/build_plot_spec.py", str(request_path), "--out", str(spec_path)],
        check=True,
        text=True,
        capture_output=True,
    )
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    assert "series" in spec["panels"][1]
    assert spec["panels"][1]["series"][0]["label"] == "Ours"

    subprocess.run(
        [
            sys.executable,
            "scripts/plot_publication_figure.py",
            str(spec_path),
            "--out-path",
            str(out_prefix),
            "--formats",
            "png",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert out_prefix.with_suffix(".png").is_file()


def test_single_scatter_request_remains_supported(tmp_path):
    request = {
        "panels": [
            {
                "kind": "scatter",
                "title": "Single Series",
                "xlabel": "Latency",
                "ylabel": "Accuracy",
                "data": {"x": [1, 2], "y": [0.8, 0.9]},
                "label": "Ours",
            }
        ]
    }
    request_path = tmp_path / "request.json"
    spec_path = tmp_path / "spec.json"
    request_path.write_text(json.dumps(request), encoding="utf-8")

    subprocess.run(
        [sys.executable, "scripts/build_plot_spec.py", str(request_path), "--out", str(spec_path)],
        check=True,
        text=True,
        capture_output=True,
    )
    panel = json.loads(spec_path.read_text(encoding="utf-8"))["panels"][0]
    assert panel["x"] == [1, 2]
    assert panel["y"] == [0.8, 0.9]
