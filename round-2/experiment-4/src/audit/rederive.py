#!/usr/bin/env python3
"""Independent re-derivation of headline numbers.

Uses a different code path from method.py:
  - route errors are recomputed from the raw columns of results/grid_values.csv (no method.py code);
  - the reference boiling temperatures are recomputed with scipy.optimize.brentq on IAPWS-IF97 directly,
    not the bisection in method.py;
  - Clapeyron residuals are recomputed from the raw per-point fields in results/clapeyron.json.
Writes audit/rederive_out.json and prints a comparison against results/summary.json.
"""
import csv
import json
from pathlib import Path

import numpy as np
from iapws import IAPWS97
from scipy.optimize import brentq

WS = Path(__file__).resolve().parent.parent
R_V = 461.5
rows = list(csv.DictReader((WS / "results" / "grid_values.csv").open()))
h = np.array([float(r["elevation_m"]) for r in rows])
tb_ref = np.array([float(r["Tb_ref_K"]) for r in rows])
tag = np.array([r["tag"] for r in rows])
summary = json.loads((WS / "results" / "summary.json").read_text())

def stats(e, mask):
    ee = e[mask]
    i = int(np.argmax(np.abs(ee)))
    return {"rms_K": float(np.sqrt(np.mean(ee**2))), "max_abs_K": float(np.abs(ee).max()),
            "altitude_of_max_m": float(h[mask][i]), "n": int(mask.sum())}

held = tag == "held_out"
full = np.ones_like(held)
out = {"routes": {}}
cols = {"constant_L_clausius_clapeyron": "err_constant_L_K", "td_L_clausius_clapeyron": "err_td_L_K",
        "antoine": "err_antoine_K"}
for name, col in cols.items():
    e = np.array([float(r[col]) for r in rows])
    out["routes"][name] = {"full": stats(e, full), "held_out": stats(e, held)}
    s_full = summary["route_errors"][name]["full_grid"]
    s_held = summary["route_errors"][name]["held_out"]
    print(f"{name}: full max {out['routes'][name]['full']['max_abs_K']:.5f} vs summary {s_full['max_abs_K']:.5f}; "
          f"held rms {out['routes'][name]['held_out']['rms_K']:.5f} vs summary {s_held['rms_K']:.5f}")

# reference: brentq on IF97 directly, independent of method.py's bisection
p_std = lambda hh: 101325.0 * (1 - 2.25577e-5 * hh) ** 5.25588
ps = lambda T: IAPWS97(T=T, x=0).P * 1e6
tb_ref_bq = np.array([brentq(lambda T, p=p_std(hh): ps(T) - p, 273.16, 373.946, xtol=1e-12) for hh in h])
gap = float(np.max(np.abs(tb_ref_bq - tb_ref)))
print(f"reference brentq vs stored Tb_ref: max gap {gap:.2e} K")
out["reference_brentq_max_gap_K"] = gap

# Clapeyron: recompute residuals from the raw fields stored per point
cl = json.loads((WS / "results" / "clapeyron.json").read_text())["points"]
rA, rB, rC = [], [], []
for p in cl:
    T, Ps, dPdT, L = p["T_K"], p["Ps_Pa"], p["dPsdT_IF97_Pa_per_K"], p["hfg_IF97_J_per_kg"]
    rv, rl = p["rho_v_IF97"], p["rho_l_IF97"]
    rA.append(dPdT * T * (R_V * T / Ps) / L - 1)
    rB.append(dPdT * T * (1 / rv) / L - 1)           # Z_v-corrected Dv equals 1/rho_v exactly
    rC.append(dPdT * T * (1 / rv - 1 / rl) / L - 1)
out["clapeyron_recomputed"] = {"max_abs_rA": float(np.max(np.abs(rA))),
                               "max_abs_rB": float(np.max(np.abs(rB))),
                               "max_abs_rC": float(np.max(np.abs(rC)))}
print("Clapeyron recomputed:", out["clapeyron_recomputed"], "| summary max|rA|",
      summary["clapeyron"]["max_abs_rA_ideal_vapour"])

# ranking check: ranking uses held-out RMS only
rk = sorted(out["routes"], key=lambda n: out["routes"][n]["held_out"]["rms_K"])
out["ranking_by_held_out_rms"] = rk
print("ranking by held-out RMS:", rk)
(WS / "audit" / "rederive_out.json").write_text(json.dumps(out, indent=2))
