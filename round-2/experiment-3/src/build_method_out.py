"""Build full_method_out.json from method.py's own functions (model-only grid).

Two methods are compared per elevation: the isothermal barometric formula and the
lapse-rate formula, each giving a predicted boiling temperature (C). No measured
observation exists in this run, so no residual against truth is computed here.
"""
import json
from pathlib import Path

import method as m

grid = [float(z) for z in range(0, 4001, 100)]
examples = []
for z in grid:
    tb_iso = m.invert_tb(m.p_isothermal(z)) - 273.15
    tb_lap = m.invert_tb(m.p_lapse(z)) - 273.15
    examples.append({
        "input": f"Site elevation {int(z)} m (standard atmosphere, model-only grid)",
        "output": f"Isothermal {tb_iso:.3f} C; lapse-rate {tb_lap:.3f} C",
        "metadata_elevation_m": str(int(z)),
        "metadata_label": "model-only; no measured observation; not validation",
        "predict_isothermal_barometric_Tb_C": f"{tb_iso:.4f}",
        "predict_lapse_rate_barometric_Tb_C": f"{tb_lap:.4f}",
    })
out = {
    "metadata": {
        "method_name": "barometric boiling-point formulas, model-only comparison",
        "description": "Two barometric formulas compared on a 100 m grid, 0-4000 m. No verified measured records (0 accepted sites); a test against measurements is UNDERPOWERED and untested.",
        "methods": ["isothermal barometric formula", "lapse-rate barometric formula"],
        "accepted_sites": 0,
        "underpowered": True,
        "source_code": "method.py",
    },
    "datasets": [{"dataset": "standard_atmosphere_grid_0_4000m_model_only", "examples": examples}],
}
Path("full_method_out.json").write_text(json.dumps(out, indent=2))
print(len(examples), "examples written")
