"""Build the boiling-point vs altitude reference dataset for gen_art_dataset_1.

Contents (all evidence_type = equation_derived; no independent measured site was
verified during web search, so the measured-site count is zero):

1. reference_grid: boiling temperature at 0-4000 m, 100 m steps, transcribed from the
   barometric-levelling table at https://www.deleze.name/marcel/en/physique/TemperaturesEbullition/table_temperature-en.html
   (values rounded to 0.1 C by the source).
2. formula_prediction: the simple barometric chain
   (a) U.S. Standard Atmosphere 1976 troposphere pressure p(h) = 101.325 kPa * (1 - 2.25577e-5 h)^5.25588
   (b) boiling point from pressure via the empirical fit used in the UC Davis / Snyder
       calibration note: T_F = 49.161 * ln(p_inHg) + 44.932 (source:
       https://ucfoodsafety.ucdavis.edu/sites/g/files/dgvnsk7366/files/inline-files/234958_1.pdf)
   compared with the reference grid as residuals.

Run:  python code/build_dataset.py   (stdlib only)
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
OUT = WS / "temp" / "datasets"
OUT.mkdir(parents=True, exist_ok=True)

ACCESS_DATE = "2026-11-21"
SRC_TABLE = (
    "Boiling water temperature in degrees C as a function of altitude (barometric levelling model), "
    "deleze.name, https://www.deleze.name/marcel/en/physique/TemperaturesEbullition/table_temperature-en.html, "
    f"accessed {ACCESS_DATE}"
)
SRC_FIT = (
    "Snyder, O. P. Jr., 'Calibrating thermometers in boiling water: Boiling Point / Atmospheric Pressure / "
    "Altitude Tables', hi-tm.com note (PDF at ucfoodsafety.ucdavis.edu), accessed " + ACCESS_DATE
)
SRC_ISA = "U.S. Standard Atmosphere 1976, NOAA/NASA/USAF, troposphere pressure relation (closed form)"

# Transcribed rows: altitude block (m) -> [t(+0), t(+100), t(+200), t(+300), t(+400)] in C
TABLE = {
    0: [100.0, 99.7, 99.3, 99.0, 98.7],
    500: [98.3, 98.0, 97.7, 97.3, 97.0],
    1000: [96.7, 96.3, 96.0, 95.7, 95.3],
    1500: [95.0, 94.7, 94.3, 94.0, 93.7],
    2000: [93.3, 93.0, 92.7, 92.3, 92.0],
    2500: [91.7, 91.3, 91.0, 90.7, 90.3],
    3000: [90.0, 89.7, 89.3, 89.0, 88.6],
    3500: [88.3, 88.0, 87.6, 87.3, 87.0],
    4000: [86.6, 86.3, 85.9, 85.6, 85.3],
}

ALTITUDE_BANDS = [(0, 500), (500, 1500), (1500, 2500), (2500, 4000)]


def band(h: float) -> str:
    for lo, hi in ALTITUDE_BANDS:
        if lo <= h < hi or (h == 4000 and hi == 4000):
            return f"{lo}-{hi} m"
    return "out_of_range"


def isa_pressure_kpa(h_m: float) -> float:
    return 101.325 * (1.0 - 2.25577e-5 * h_m) ** 5.25588


def fit_boiling_c(p_kpa: float) -> float:
    p_inhg = p_kpa / 3.38639
    t_f = 49.161 * math.log(p_inhg) + 44.932
    return (t_f - 32.0) * 5.0 / 9.0


def reference_rows() -> list[dict]:
    rows = []
    for base, vals in TABLE.items():
        for j, t in enumerate(vals):
            h = base + 100 * j
            if h > 4000:
                continue
            rows.append(
                {
                    "site_id": f"REF-{h:04d}m",
                    "site_name": f"Reference grid {h} m",
                    "country": None,
                    "latitude": None,
                    "longitude": None,
                    "elevation_m": float(h),
                    "elevation_uncertainty_m": None,
                    "station_pressure_kPa": None,
                    "pressure_source": None,
                    "pressure_date": None,
                    "boiling_temp_C": t,
                    "boiling_temp_uncertainty_C": 0.05,
                    "thermometer_description": None,
                    "measurement_method": "barometric levelling model (table lookup)",
                    "evidence_type": "equation_derived",
                    "source_citation": SRC_TABLE,
                    "split": "reference",
                    "drop_reason": None,
                    "altitude_band": band(h),
                    "formula_pressure_kPa": round(isa_pressure_kpa(h), 3),
                    "formula_boiling_C": round(fit_boiling_c(isa_pressure_kpa(h)), 2),
                    "formula_residual_C": round(fit_boiling_c(isa_pressure_kpa(h)) - t, 2),
                }
            )
    return rows


def main() -> None:
    rows = reference_rows()
    residuals = [r["formula_residual_C"] for r in rows]
    summary = {
        "n_rows": len(rows),
        "n_measured_sites": 0,
        "n_equation_derived_rows": sum(r["evidence_type"] == "equation_derived" for r in rows),
        "altitude_range_m": [min(r["elevation_m"] for r in rows), max(r["elevation_m"] for r in rows)],
        "holdout_rule": (
            "Predefined before data collection: hold out all measured sites in the Americas above 1000 m. "
            "No measured sites were verified, so the holdout set is empty."
        ),
        "formula_vs_table_residual_C": {
            "mean": round(sum(residuals) / len(residuals), 3),
            "max_abs": round(max(abs(x) for x in residuals), 3),
        },
        "sources": {"reference_table": SRC_TABLE, "formula_fit": SRC_FIT, "pressure_model": SRC_ISA},
    }
    with (OUT / "boiling_point_altitude_full.json").open("w") as f:
        json.dump(rows, f, indent=2)
    mini = rows[:5]
    preview = [{k: (v[:200] if isinstance(v, str) else v) for k, v in r.items()} for r in rows[:5]]
    with (OUT / "boiling_point_altitude_mini.json").open("w") as f:
        json.dump(mini, f, indent=2)
    with (OUT / "boiling_point_altitude_preview.json").open("w") as f:
        json.dump(preview, f, indent=2)
    with (OUT / "boiling_point_altitude.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with (OUT / "summary.json").open("w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
