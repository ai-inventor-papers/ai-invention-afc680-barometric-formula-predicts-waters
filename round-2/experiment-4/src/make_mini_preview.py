#!/usr/bin/env python3
"""Write mini (first 3 examples) and preview (mini with strings cut to 200 chars) variants of results/method_out.json."""
import copy
import json
from pathlib import Path

WS = Path(__file__).resolve().parent
src = WS / "full_method_out.json"
data = json.loads(src.read_text())


def truncate(obj):
    if isinstance(obj, str):
        return obj if len(obj) <= 200 else obj[:200] + "..."
    if isinstance(obj, list):
        return [truncate(x) for x in obj]
    if isinstance(obj, dict):
        return {k: truncate(v) for k, v in obj.items()}
    return obj


mini = copy.deepcopy(data)
mini["datasets"][0]["examples"] = mini["datasets"][0]["examples"][:3]
preview = truncate(copy.deepcopy(mini))
(WS / "mini_method_out.json").write_text(json.dumps(mini, indent=2))
(WS / "preview_method_out.json").write_text(json.dumps(preview, indent=2))
print("mini examples:", len(mini["datasets"][0]["examples"]))
