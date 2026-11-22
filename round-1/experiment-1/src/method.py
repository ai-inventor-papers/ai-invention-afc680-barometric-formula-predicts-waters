#!/usr/bin/env python3
"""Barometric boiling-point screen on a 0-4000 m grid (100 m steps).

Compares two barometric pressure forms (isothermal and standard lapse-rate)
against a reference built from U.S. Standard Atmosphere 1976 pressures.
Boiling temperatures come from the Wagner-Pruss (IAPWS vapour-pressure)
equation, inverted by bisection. No field measurements are used.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np
from loguru import logger

WS = Path(__file__).resolve().parent
(WS / "logs").mkdir(exist_ok=True)
(WS / "results").mkdir(exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(WS / "logs" / "run.log", rotation="30 MB", level="DEBUG")
logger.add(WS / "results" / "log.txt", level="DEBUG")

# ---------------- Constants ----------------
G0 = 9.80665            # m/s^2
R_AIR = 287.05287       # J/(kg K)
T0 = 288.15             # K, sea-level standard temperature
LAPSE = 0.0065          # K/m, tropospheric lapse rate
P0 = 101325.0           # Pa
TC = 647.096            # K, critical temperature of water
PC = 22.064e6           # Pa, critical pressure of water

# Wagner and Pruss (2002) vapour-pressure equation coefficients (IAPWS).
WP_N = np.array([-7.85951783, 1.84408259, -11.7866497,
                 22.6807411, -15.9618719, 1.80122502])
WP_EXP = np.array([1.0, 1.5, 3.0, 3.5, 4.0, 7.5])

# USSA 1976 pressure nodes (geopotential m -> Pa), recalled from the standard table.
USSA_NODES_M = np.array([0.0, 1000.0, 2000.0, 3000.0, 4000.0])
USSA_NODES_PA = np.array([101325.0, 89875.0, 79501.0, 70108.0, 61640.0])

Z_GRID = np.arange(0.0, 4000.0 + 100.0, 100.0)  # 41 points
ERR_LIMIT_K = 0.6                                # plan's pass/fail limit (K)
BORDERLINE_MARGIN_K = 0.05


# ---------------- Physics ----------------
def psat(t_kelvin: np.ndarray) -> np.ndarray:
    """Saturation vapour pressure (Pa) from the Wagner-Pruss equation."""
    t = np.asarray(t_kelvin, dtype=float)
    tau = 1.0 - t / TC
    series = np.zeros_like(tau)
    for coef, expo in zip(WP_N, WP_EXP):
        series = series + coef * tau ** expo
    return PC * np.exp((TC / t) * series)


def tsat(p_pa: np.ndarray) -> np.ndarray:
    """Boiling temperature (K) at pressure p, by vectorised bisection (80 iterations)."""
    p = np.asarray(p_pa, dtype=float)
    lo = np.full_like(p, 273.16)
    hi = np.full_like(p, 647.0)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        above = psat(mid) > p
        hi = np.where(above, mid, hi)
        lo = np.where(above, lo, mid)
    return 0.5 * (lo + hi)


def p_isothermal(z: np.ndarray) -> np.ndarray:
    return P0 * np.exp(-G0 * z / (R_AIR * T0))


def p_lapse(z: np.ndarray) -> np.ndarray:
    return P0 * (1.0 - LAPSE * z / T0) ** (G0 / (R_AIR * LAPSE))


# ---------------- Tests (run in order, stop at first failure) ----------------
class TestFailure(RuntimeError):
    pass


def check(name: str, ok: bool, detail: str, records: list[dict]) -> None:
    records.append({"test": name, "passed": bool(ok), "detail": detail})
    if ok:
        logger.info(f"PASS {name}: {detail}")
    else:
        logger.error(f"FAIL {name}: {detail}")
        raise TestFailure(f"{name} failed: {detail}")


def run_tests(records: list[dict]) -> dict:
    # T1 saturation check
    tb_sea = float(tsat(np.array([P0]))[0])
    check("T1_saturation_101325Pa", abs(tb_sea - 373.124) <= 0.005,
          f"Tb(101325 Pa) = {tb_sea:.4f} K = {tb_sea - 273.15:.4f} C (target 373.124 K)", records)
    tb_100c = float(tsat(np.array([101420.0]))[0]) - 273.15
    check("T1b_about_100C_at_101420Pa", abs(tb_100c - 100.0) <= 0.01,
          f"Tb(101420 Pa) = {tb_100c:.4f} C (target 100.00 C)", records)

    # T2 round trip
    p_test = np.linspace(40e3, 101e3, 200)
    rt = psat(tsat(p_test)) / p_test - 1.0
    max_rt = float(np.max(np.abs(rt)))
    check("T2_round_trip", max_rt <= 1e-6,
          f"max relative error of Psat(Tb(p)) over 40-101 kPa = {max_rt:.2e}", records)

    # T3 monotonicity (computed later on the grid, after the arrays exist)
    # T4 standard-atmosphere check
    rel_nodes = np.abs(p_lapse(USSA_NODES_M) / USSA_NODES_PA - 1.0)
    logger.info("Node check p_lapse vs USSA table: " +
                ", ".join(f"{z:.0f} m: {100 * r:.4f}%" for z, r in zip(USSA_NODES_M, rel_nodes)))
    check("T4a_lapse_matches_USSA_nodes", float(np.max(rel_nodes)) <= 0.002,
          f"max node deviation = {100 * float(np.max(rel_nodes)):.4f}% (limit 0.2%)", records)
    z_pos = Z_GRID[1:]
    check("T4b_isothermal_exceeds_lapse_above_0", bool(np.all(p_isothermal(z_pos) > p_lapse(z_pos))),
          "p_iso > p_lapse at every z > 0", records)
    return {"tb_sea_K": tb_sea, "tb_100C_check_C": tb_100c, "max_roundtrip_rel": max_rt,
            "max_node_rel_dev": float(np.max(rel_nodes))}


def main() -> None:
    logger.info("Starting barometric boiling-point screen (41-point grid, 0-4000 m)")
    records: list[dict] = []
    t_checks = run_tests(records)

    z = Z_GRID
    p_iso = p_isothermal(z)
    p_lap = p_lapse(z)
    p_ref = p_lap.copy()  # USSA troposphere definition (plan STEP 2)

    tb_ref = tsat(p_ref)
    tb_iso = tsat(p_iso)
    tb_lap = tsat(p_lap)
    s_struct = tb_iso - tb_lap
    err_iso = tb_iso - tb_ref
    err_lap = tb_lap - tb_ref

    # T3 monotonicity
    for name, arr in [("reference", tb_ref), ("isothermal", tb_iso), ("lapse", tb_lap)]:
        check(f"T3_monotonic_{name}", bool(np.all(np.diff(arr) < 0)),
              "boiling T decreases with altitude at every 100 m step", records)

    # T5 sea level
    check("T5_sea_level_consistency",
          abs(tb_iso[0] - 373.124) <= 0.005 and abs(tb_lap[0] - 373.124) <= 0.005
          and abs(tb_ref[0] - 373.124) <= 0.005 and s_struct[0] == 0.0,
          f"T_iso(0)={tb_iso[0]:.4f} K, T_lap(0)={tb_lap[0]:.4f} K, T_ref(0)={tb_ref[0]:.4f} K, s(0)={s_struct[0]:.3f}",
          records)

    # T6 sign and size
    def s_at(zm: float) -> float:
        return float(s_struct[int(round(zm / 100.0))])

    s3000, s4000 = s_at(3000.0), s_at(4000.0)
    check("T6_structural_term_size",
          abs(s3000 - 0.3) <= 0.1 and abs(s4000 - 0.55) <= 0.1,
          f"s(3000 m)={s3000:.3f} K (expect ~0.3), s(4000 m)={s4000:.3f} K (expect ~0.5-0.6)", records)

    # T7 cross-check against the IAPWS package (IF97 region 4, saturated liquid)
    cross_idx = [0, 20, 40]
    cross_status = "not run"
    cross_max_diff = None
    try:
        from iapws import IAPWS97
        diffs = []
        for i in cross_idx:
            t_iapws = IAPWS97(P=p_ref[i] / 1e6, x=0).T
            diffs.append(abs(t_iapws - tb_ref[i]))
            logger.info(f"Cross-check z={z[i]:.0f} m: iapws T={t_iapws:.4f} K, ours T={tb_ref[i]:.4f} K")
        cross_max_diff = float(max(diffs))
        cross_status = "iapws IF97 region 4"
        check("T7_crosscheck_iapws", cross_max_diff <= 0.01,
              f"max |difference| at 0, 2000, 4000 m = {cross_max_diff:.5f} K (limit 0.01 K)", records)
    except ImportError:
        logger.warning("iapws package not importable; cross-check T7 skipped (Antoine not used: "
                       "its stated range does not cover this grid reliably).")

    # Metrics
    max_iso_i = int(np.argmax(np.abs(err_iso)))
    max_lap_i = int(np.argmax(np.abs(err_lap)))
    max_iso = float(np.abs(err_iso)[max_iso_i])
    max_lap = float(np.abs(err_lap)[max_lap_i])
    rms_iso = float(np.sqrt(np.mean(err_iso ** 2)))
    rms_lap = float(np.sqrt(np.mean(err_lap ** 2)))

    def verdict(max_err: float) -> dict:
        survives = max_err <= ERR_LIMIT_K
        borderline = abs(max_err - ERR_LIMIT_K) <= BORDERLINE_MARGIN_K
        label = "borderline: no pass/fail claim" if borderline else ("pass" if survives else "fail")
        return {"limit_K": ERR_LIMIT_K, "max_abs_err_K": max_err,
                "margin_K": ERR_LIMIT_K - max_err, "label": label}

    summary = {
        "title": "Checking barometric boiling-point formulas on a grid",
        "reference": {
            "pressure": "USSA 1976 troposphere (p_lapse, nodes verified against tabulated values)",
            "saturation": "Wagner-Pruss (IAPWS) equation, bisection inversion",
            "cross_check": cross_status,
            "cross_check_max_diff_K": cross_max_diff,
        },
        "constants": {"g0": G0, "R_air": R_AIR, "T0": T0, "L": LAPSE, "p0": P0},
        "scale_height_isothermal_m": R_AIR * T0 / G0,
        "tests": records,
        "tests_passed": all(r["passed"] for r in records),
        "t_checks": t_checks,
        "at_altitude": {
            f"{int(zz)}m": {
                "structural_s_K": float(s_struct[int(zz / 100)]),
                "err_isothermal_K": float(err_iso[int(zz / 100)]),
                "err_lapse_K": float(err_lap[int(zz / 100)]),
            } for zz in [1000, 2000, 3000, 4000]
        },
        "max_abs_err_isothermal": {"value_K": max_iso, "altitude_m": float(z[max_iso_i])},
        "max_abs_err_lapse": {"value_K": max_lap, "altitude_m": float(z[max_lap_i])},
        "rms_err_isothermal_K": rms_iso,
        "rms_err_lapse_K": rms_lap,
        "verdict_isothermal": verdict(max_iso),
        "verdict_lapse": verdict(max_lap),
        "note_lapse_is_reference": (
            "The lapse-rate form is the reference pressure model itself (USSA troposphere), "
            "so err_lapse is zero by construction and the only informative error is the "
            "isothermal form against the reference."
        ),
        "no_field_measurements": True,
    }

    # Write grid CSV (all intermediates)
    csv_path = WS / "results" / "grid_values.csv"
    with csv_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["z_m", "p_isothermal_Pa", "p_lapse_Pa", "p_ussa_ref_Pa",
                    "Tb_ref_C", "Tb_isothermal_C", "Tb_lapse_C",
                    "structural_s_K", "err_isothermal_K", "err_lapse_K"])
        for i in range(len(z)):
            w.writerow([f"{z[i]:.1f}", f"{p_iso[i]:.3f}", f"{p_lap[i]:.3f}", f"{p_ref[i]:.3f}",
                        f"{tb_ref[i] - 273.15:.5f}", f"{tb_iso[i] - 273.15:.5f}",
                        f"{tb_lap[i] - 273.15:.5f}", f"{s_struct[i]:.6f}",
                        f"{err_iso[i]:.6f}", f"{err_lap[i]:.6f}"])
    logger.info(f"Wrote {csv_path}")

    # Write summary
    (WS / "results" / "summary.json").write_text(json.dumps(summary, indent=2))
    logger.info(f"Wrote summary.json; isothermal max|err|={max_iso:.3f} K at {z[max_iso_i]:.0f} m "
                f"-> {verdict(max_iso)['label']}; RMS={rms_iso:.3f} K")

    # Write output in the exp_gen_sol_out schema
    examples = []
    for i in range(len(z)):
        examples.append({
            "input": f"Altitude z = {z[i]:.0f} m (geopotential). Predict the boiling point of water.",
            "output": f"{tb_ref[i] - 273.15:.3f} C (USSA 1976 pressure, Wagner-Pruss inversion)",
            "metadata_altitude_m": float(z[i]),
            "metadata_pressure_ref_Pa": float(p_ref[i]),
            "predict_isothermal": f"{tb_iso[i] - 273.15:.3f} C",
            "predict_lapse_rate": f"{tb_lap[i] - 273.15:.3f} C",
        })
    out = {
        "metadata": {
            "method_name": "barometric boiling-point formulas vs USSA reference",
            "description": "Isothermal and lapse-rate barometric forms compared on a 0-4000 m grid.",
        },
        "datasets": [{"dataset": "ussa1976_grid_0_4000m", "examples": examples}],
    }
    (WS / "results" / "method_out.json").write_text(json.dumps(out, indent=2))
    logger.info("Wrote results/method_out.json")
    logger.info("Done.")


if __name__ == "__main__":
    try:
        main()
    except TestFailure:
        logger.error("Stopped at first failing test; no results written beyond the failure.")
        raise
