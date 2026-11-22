#!/usr/bin/env python3
"""Standardize boiling-point source records into the exp_sel_data_out format.

Reads temp/datasets/measured_boiling_point_records_full.json (measured tiers A/B; currently empty)
and the Tier C reference rows stated in the Snyder altitude table. Writes full_data_out.json.
Standard library only, so it runs as `uv run data.py` with no extra dependencies.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATASETS_DIR = ROOT / "temp" / "datasets"
MEASURED_PATH = DATASETS_DIR / "measured_boiling_point_records_full.json"
OUT_PATH = ROOT / "full_data_out.json"
SNYDER_URL = "https://ucfoodsafety.ucdavis.edu/sites/g/files/dgvnsk7366/files/inline-files/234958_1.pdf"
ACCESS_DATE = "2026-11-22"


def log(message: str) -> None:
    print(message, flush=True)


def f_to_c(temp_f: float) -> float:
    return round((temp_f - 32.0) * 5.0 / 9.0, 2)


def measured_examples() -> list[dict]:
    """Tier A/B rows from the measured-records file, one example per record."""
    data = json.loads(MEASURED_PATH.read_text())
    examples = []
    for i, rec in enumerate(data.get("records", [])):
        examples.append(
            {
                "input": json.dumps(
                    {
                        "site_name": rec["site_name"],
                        "elevation_m": rec["elevation_m"],
                        "elevation_unc_m": rec["elevation_unc_m"],
                        "station_pressure_kPa": rec["station_pressure_kPa"],
                    },
                    sort_keys=True,
                ),
                "output": str(rec["boiling_temp_C"]),
                "metadata_row_index": i,
                "metadata_tier": rec["tier"],
                "metadata_thermometer_unc_C": rec["thermometer_unc_C"],
                "metadata_citation": rec["citation"],
                "metadata_task_type": "regression",
            }
        )
    return examples


def reference_examples() -> list[dict]:
    """Tier C: boiling points stated in the Snyder table (equation-derived, reference only)."""
    stated_f = [(0, 212.0), (1000, 210.2), (2000, 208.4), (3000, 206.6)]
    examples = []
    for i, (elev_ft, boil_f) in enumerate(stated_f):
        examples.append(
            {
                "input": json.dumps({"elevation_ft": elev_ft, "pressure_source": "none stated"}, sort_keys=True),
                "output": str(f_to_c(boil_f)),
                "metadata_row_index": i,
                "metadata_tier": "C",
                "metadata_measured": False,
                "metadata_citation": f"Snyder, O. P. Jr., {SNYDER_URL}, accessed {ACCESS_DATE}",
                "metadata_task_type": "regression",
            }
        )
    return examples


def main() -> None:
    groups = []
    measured = measured_examples()
    if measured:
        groups.append({"dataset": "measured_boiling_point_records", "examples": measured})
    else:
        log("No measured Tier A/B records found; the measured group is omitted.")
    groups.append({"dataset": "snyder_altitude_boiling_reference_tierC", "examples": reference_examples()})

    output = {
        "metadata": {
            "title": "Measured Boiling-Point Records by Altitude (standardized)",
            "measured_rows": len(measured),
            "tier_C_rows": len(groups[-1]["examples"]),
            "note": "Tier C rows are equation-derived reference values, not measurements.",
        },
        "datasets": groups,
    }
    OUT_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    log(f"Wrote {OUT_PATH} with {len(measured)} measured and {len(groups[-1]['examples'])} tier C examples")
    write_variants(output)


def truncate_strings(node, limit: int = 200):
    """Recursively cut every string to `limit` characters (preview variant)."""
    if isinstance(node, str):
        return node if len(node) <= limit else node[:limit] + "..."
    if isinstance(node, list):
        return [truncate_strings(x, limit) for x in node]
    if isinstance(node, dict):
        return {k: truncate_strings(v, limit) for k, v in node.items()}
    return node


def write_variants(output: dict) -> None:
    """mini = first 3 examples per dataset group; preview = mini with strings cut to 200 chars.

    Written here instead of with aii-json's format script, which only accepts paths under
    the project directory or /tmp and therefore cannot read files in this workspace.
    """
    mini = {
        "metadata": output["metadata"],
        "datasets": [
            {"dataset": g["dataset"], "examples": g["examples"][:3]} for g in output["datasets"]
        ],
    }
    (ROOT / "mini_data_out.json").write_text(json.dumps(mini, indent=2, ensure_ascii=False))
    (ROOT / "preview_data_out.json").write_text(
        json.dumps(truncate_strings(mini), indent=2, ensure_ascii=False)
    )
    log("Wrote mini_data_out.json and preview_data_out.json")


if __name__ == "__main__":
    main()
