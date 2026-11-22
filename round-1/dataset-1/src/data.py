# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Convert the boiling-point vs altitude reference table into the exp_sel_data_out format.

Input : temp/datasets/boiling_point_altitude_full.json   (one record per altitude)
Output: full_data_out.json       (exp_sel_data_out, grouped by dataset, one example per row)
        mini_data_out.json       (first 3 examples per dataset)
        preview_data_out.json    (mini, strings truncated to 200 characters)

Only one candidate dataset was verified (the equation-derived reference grid); no measured
boiling records were found, so there is one dataset group. Each row is one example.
Input field = altitude only (no formula or table values, to avoid leaking the target).
Output field = observed (table) boiling temperature in C as a string.
"""

from __future__ import annotations

import json
from pathlib import Path

WS = Path(__file__).resolve().parent
SRC = WS / "temp" / "datasets" / "boiling_point_altitude_full.json"
DATASET_NAME = "boiling_point_altitude_reference_grid"


def to_example(rec: dict, i_row: int) -> dict:
    return {
        "input": json.dumps({"elevation_m": rec["elevation_m"]}, sort_keys=True),
        "output": f"{rec['boiling_temp_C']:.1f}",
        "metadata_site_id": rec["site_id"],
        "metadata_evidence_type": rec["evidence_type"],
        "metadata_split": rec["split"],
        "metadata_altitude_band": rec["altitude_band"],
        "metadata_boiling_temp_uncertainty_C": rec["boiling_temp_uncertainty_C"],
        "metadata_formula_boiling_C": rec["formula_boiling_C"],
        "metadata_formula_residual_C": rec["formula_residual_C"],
        "metadata_source_citation": rec["source_citation"],
        "metadata_row_index": i_row,
    }


def build(records: list[dict]) -> dict:
    examples = [to_example(rec, i) for i, rec in enumerate(records)]
    return {
        "metadata": {
            "description": "Boiling temperature of water vs elevation; equation-derived reference grid. "
            "No measured sites verified; measured_site_count = 0.",
            "holdout_rule": "Predefined: hold out measured sites in the Americas above 1000 m. Empty in this release.",
            "measured_site_count": 0,
        },
        "datasets": [{"dataset": DATASET_NAME, "examples": examples}],
    }


def truncate(obj):
    if isinstance(obj, str):
        return obj[:200]
    if isinstance(obj, list):
        return [truncate(x) for x in obj]
    if isinstance(obj, dict):
        return {k: truncate(v) for k, v in obj.items()}
    return obj


def main() -> None:
    records = json.loads(SRC.read_text())
    full = build(records)
    mini = {
        **{k: v for k, v in full.items() if k != "datasets"},
        "datasets": [{"dataset": d["dataset"], "examples": d["examples"][:3]} for d in full["datasets"]],
    }
    preview = truncate(mini)
    (WS / "full_data_out.json").write_text(json.dumps(full, indent=2))
    (WS / "mini_data_out.json").write_text(json.dumps(mini, indent=2))
    (WS / "preview_data_out.json").write_text(json.dumps(preview, indent=2))
    n = sum(len(d["examples"]) for d in full["datasets"])
    print(f"wrote {n} examples across {len(full['datasets'])} dataset group(s)")


if __name__ == "__main__":
    main()
