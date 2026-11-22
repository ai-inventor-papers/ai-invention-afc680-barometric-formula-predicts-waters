#!/usr/bin/env python3
"""Independent re-derivation of the headline numbers from the raw CSV.

Different code path from method.py: boiling temperatures come from the iapws
package (IAPWS-97, region 4) applied to the pressures stored in
results/grid_values.csv, not from the Wagner-Pruss bisection in method.py.
A constant-pressure placebo checks that the error metric discriminates.
"""

import csv
import sys
from pathlib import Path

from iapws import IAPWS97
from loguru import logger

WS = Path(__file__).resolve().parent
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

rows = list(csv.DictReader((WS / "results" / "grid_values.csv").open()))
P_SEA = 101325.0


def tb_c(p_pa: float) -> float:
    """Saturated-liquid temperature (deg C) at pressure p, via IAPWS-97."""
    return IAPWS97(P=p_pa / 1e6, x=0).T - 273.15


z = [float(r["z_m"]) for r in rows]
p_iso = [float(r["p_isothermal_Pa"]) for r in rows]
p_lap = [float(r["p_lapse_Pa"]) for r in rows]
p_ref = [float(r["p_ussa_ref_Pa"]) for r in rows]

tb_ref = [tb_c(p) for p in p_ref]
tb_iso = [tb_c(p) for p in p_iso]
tb_lap = [tb_c(p) for p in p_lap]
err_iso = [a - b for a, b in zip(tb_iso, tb_ref)]
s_struct = [a - b for a, b in zip(tb_iso, tb_lap)]

max_i = max(range(len(z)), key=lambda i: abs(err_iso[i]))
logger.info(f"Independent max|err_iso| = {abs(err_iso[max_i]):.4f} K at {z[max_i]:.0f} m")
logger.info(f"Independent s(3000 m) = {s_struct[30]:.4f} K, s(4000 m) = {s_struct[40]:.4f} K")
rms = (sum(e * e for e in err_iso) / len(err_iso)) ** 0.5
logger.info(f"Independent RMS err_iso = {rms:.4f} K")

csv_err = [float(r["err_isothermal_K"]) for r in rows]
max_diff = max(abs(a - b) for a, b in zip(err_iso, csv_err))
logger.info(f"Max abs difference vs method.py err_isothermal_K = {max_diff:.5f} K")

# Placebo: a constant sea-level pressure (no altitude dependence) must produce a large error
tb_sea = tb_c(P_SEA)
placebo_err = [tb_sea - t for t in tb_ref]
logger.info(f"Placebo (constant {P_SEA:.0f} Pa) max|err| = {max(abs(x) for x in placebo_err):.2f} K "
            "(should be far above 0.6 K, showing the metric discriminates)")
