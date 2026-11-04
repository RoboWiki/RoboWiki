from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_validate_passes():
    r = subprocess.run(
        [sys.executable, "-m", "pipeline", "validate"],
        capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT),
        env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"},
    )
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-2000:]


def test_counts_are_stable():
    from pipeline.load import load_parts

    parts = load_parts()
    assert len(parts) == 339
    robots = []
    for p in sorted((ROOT / "data" / "robots").glob("*.json")):
        robots.extend(json.loads(p.read_text(encoding="utf-8")))
    assert len(robots) == 21
    sw = json.loads((ROOT / "data" / "software.json").read_text(encoding="utf-8"))
    assert len(sw["items"]) == 22
    sups = json.loads((ROOT / "data" / "suppliers.json").read_text(encoding="utf-8"))
    assert len(sups) == 207
