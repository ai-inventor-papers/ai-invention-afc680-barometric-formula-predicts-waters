#!/usr/bin/env python3
"""Write full, mini and preview variants of method_out.json.

The aii-json formatter only accepts a top-level array, and method_out.json is an
object (metadata + datasets[].examples). The same rule is applied to the examples:
  full    - identical to method_out.json
  mini    - metadata kept, first 3 examples of each dataset
  preview - mini with every string truncated to 200 characters
"""

import copy
import json
import sys
from pathlib import Path

from loguru import logger

WS = Path(__file__).resolve().parent
SRC = WS / "method_out.json"
MAX_STR = 200
N_MINI = 3


def truncate(obj):
    if isinstance(obj, str):
        return obj if len(obj) <= MAX_STR else obj[:MAX_STR] + "..."
    if isinstance(obj, list):
        return [truncate(x) for x in obj]
    if isinstance(obj, dict):
        return {k: truncate(v) for k, v in obj.items()}
    return obj


def main() -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    data = json.loads(SRC.read_text())
    full = data
    mini = copy.deepcopy(data)
    for ds in mini["datasets"]:
        ds["examples"] = ds["examples"][:N_MINI]
    preview = truncate(copy.deepcopy(mini))
    for name, obj in [("full", full), ("mini", mini), ("preview", preview)]:
        out = WS / f"{name}_method_out.json"
        out.write_text(json.dumps(obj, indent=2))
        n = sum(len(d["examples"]) for d in obj["datasets"])
        logger.info(f"Wrote {out.name} ({n} examples)")


if __name__ == "__main__":
    main()
