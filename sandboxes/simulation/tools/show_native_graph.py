#!/usr/bin/env python3
"""Print every runtime simulation graph node and edge as JSON."""

from __future__ import annotations

import json
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app.simulation.native_graph import GRAPH


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--beams",
        action="store_true",
        help="include the ordered runtime graph-route observations",
    )
    args = parser.parse_args()
    snapshot = GRAPH.snapshot()
    if args.beams:
        snapshot["beam_observations"] = GRAPH.beam_observations()
    print(json.dumps(snapshot, indent=2, sort_keys=True))
