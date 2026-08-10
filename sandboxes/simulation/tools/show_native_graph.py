#!/usr/bin/env python3
"""Print every runtime simulation graph node and edge as JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app.simulation.native_graph import GRAPH


if __name__ == "__main__":
    print(json.dumps(GRAPH.snapshot(), indent=2, sort_keys=True))
