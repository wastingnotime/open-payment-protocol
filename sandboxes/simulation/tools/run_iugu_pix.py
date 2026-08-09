#!/usr/bin/env python3
"""Run the Iugu first-slice scenarios and emit a canonical JSON report."""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from app.simulation.scenarios import run_all  # noqa: E402


def main() -> None:
    print(json.dumps({name: result.__dict__ for name, result in run_all().items()}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
