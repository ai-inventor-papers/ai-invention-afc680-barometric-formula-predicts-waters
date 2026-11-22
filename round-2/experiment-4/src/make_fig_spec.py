#!/usr/bin/env python3
"""Build the error-vs-altitude line spec from results/grid_values.csv (raw values only)."""
import csv
import json
from pathlib import Path

WS = Path(__file__).resolve().parent
rows = list(csv.DictReader((WS / "results" / "grid_values.csv").open()))
alt = [float(r["elevation_m"]) for r in rows]
spec = {
    "type": "line",
    "title": "Boiling-temperature error against IF97 reference",
    "xlabel": "Altitude (m)",
    "ylabel": "Error vs IF97 boiling temperature (K)",
    "aspect": "16:9",
    "series": [
        {"label": "Constant-L Clausius-Clapeyron", "x": alt,
         "values": [float(r["err_constant_L_K"]) for r in rows]},
        {"label": "Temperature-dependent-L Clausius-Clapeyron", "x": alt,
         "values": [float(r["err_td_L_K"]) for r in rows]},
        {"label": "Antoine (fit 273.15-363.15 K)", "x": alt,
         "values": [float(r["err_antoine_K"]) for r in rows]},
    ],
}
out = WS / "figures" / "fig_error_vs_altitude_spec.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(spec, indent=2))
print("wrote", out)
