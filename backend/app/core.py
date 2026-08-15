from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "backend" / "artifacts"
DATA = ROOT / "data" / "demo"
RESULTS = ROOT / "results"
DATABASE_URL = os.getenv("PAEI_DATABASE_URL", f"sqlite:///{ROOT / 'energy_intelligence.db'}")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))
