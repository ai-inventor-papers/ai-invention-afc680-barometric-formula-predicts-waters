#!/usr/bin/env python3
"""Held-out test of three vapour-pressure routes for water boiling temperature,
and a Clapeyron consistency check, against the IAPWS-IF97 saturation curve.

Routes (each maps altitude -> standard-atmosphere pressure -> boiling temperature
by bisection on its own saturation-pressure function):
  1. constant-latent-heat Clausius-Clapeyron, anchored at 373.124 K, 101325 Pa
  2. temperature-dependent-latent-heat Clausius-Clapeyron (integrated numerically)
  3. Antoine equation, constants fitted on 273.15-363.15 K (held-out 363.15-373.15 K)

Only model-to-reference comparisons are made. No measured boiling records are read.
"""

from __future__ import annotations

import csv
import json
import math
import resource
import sys
import time
from pathlib import Path

import numpy as np
from iapws import IAPWS95, IAPWS97
from loguru import logger
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import least_squares

WS = Path(__file__).resolve().parent
LOG_DIR = WS / "logs"
RES_DIR = WS / "results"
DATA_DIR = WS / "data"
for _d in (LOG_DIR, RES_DIR, DATA_DIR):
    _d.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOG_DIR / "run.log", rotation="30 MB", level="DEBUG")

# ---- constants -------------------------------------------------------------
R_V = 461.5                 # J/(kg K), specific gas constant of water vapour
T0 = 373.124                # K, normal boiling point anchor
P0 = 101325.0               # Pa
T_TRIPLE = 273.16
T_CRIT = 373.946
GRID_H = np.arange(0, 4001, 50).astype(float)   # 81 altitudes, m
FIT_LO, FIT_HI = 273.15, 363.15                  # Antoine fit range (K)
HELD_LO, HELD_HI = 363.15, 373.15                # held-out band (K), by Tb_ref
SENS_FIT_HI = 353.15                             # sensitivity fit upper limit (K)
SENS_HELD_LO = 353.15                            # sensitivity held-out lower (K)
BISECT_TOL = 1e-9           # K
SURVIVAL_MAX_K = 0.6        # max full-grid error for survival, K
CL_TOL = 0.01               # Clapeyron tolerance (relative)
DT_DIFF = 0.01              # K, step for dPs/dT
ANTOINE_P0 = (10.19625, 1730.63, -39.724)   # log10(Pa), B, C(K), NIST water, converted

# prior-screen regression targets (from the plan's prior results)
REG_TARGETS = {
    "constant_L_max_K": 0.278,
    "constant_L_rms_K": 0.152,
    "td_L_max_K": 0.177,
    "td_L_rms_K": 0.108,
    "antoine_in_sample_max_K": 0.0042,
    "antoine_in_sample_rms_K": 0.0022,
    "clapeyron_ideal_max_pct": 1.59,
}
REG_TOL_K = 0.005
REG_TOL_PCT = 0.05

# Cross-check input: a copy of the full table of dependency art__Ga8TbdhmlP8
# (Water Boiling Temperature by Elevation Reference Table), kept under data/.
DATASET_FILE = DATA_DIR / "full_data_out.json"


def _rel(path: Path) -> str:
    """Workspace-relative path for logs, so no absolute server path is written."""
    return str(path.relative_to(WS))


# ---- standard atmosphere ------------------------------------------------------
def p_std(h_m: float) -> float:
    """U.S. Standard Atmosphere 1976 troposphere pressure, Pa."""
    return 101325.0 * (1.0 - 2.25577e-5 * h_m) ** 5.25588


def t_std(h_m: float) -> float:
    """U.S. Standard Atmosphere 1976 troposphere temperature, K."""
    return 288.15 - 0.0065 * h_m


# ---- reference: IAPWS-IF97 region 4 (saturation) -------------------------------
def ps_ref(T: float) -> float:
    """Saturation pressure, Pa (IAPWS-IF97 region 4)."""
    return IAPWS97(T=T, x=0).P * 1e6


def sat_if97(T: float) -> dict:
    """Saturation properties at T from IF97: P (Pa), h_fg (J/kg), rho_l, rho_v (kg/m3)."""
    liq = IAPWS97(T=T, x=0)
    vap = IAPWS97(T=T, x=1)
    return {
        "P": vap.P * 1e6,
        "hfg": (vap.h - liq.h) * 1e3,
        "rho_l": liq.rho,
        "rho_v": vap.rho,
    }


def invert_T(p_func, p: float, lo: float = T_TRIPLE, hi: float = T_CRIT) -> float:
    """Bisection: find T with p_func(T) = p, to width BISECT_TOL K."""
    a, b = lo, hi
    if not (p_func(a) <= p <= p_func(b)):
        raise ValueError(f"target pressure {p} Pa outside bracket")
    while b - a > BISECT_TOL:
        m = 0.5 * (a + b)
        if p_func(m) < p:
            a = m
        else:
            b = m
    return 0.5 * (a + b)


# ---- route 1: constant-L Clausius-Clapeyron ---------------------------------------
def make_route_const(L_const: float):
    def p_route(T: float) -> float:
        return P0 * math.exp(-(L_const / R_V) * (1.0 / T - 1.0 / T0))
    return p_route


# ---- route 2: temperature-dependent-L Clausius-Clapeyron -----------------------------
def build_td_table() -> tuple[np.ndarray, np.ndarray]:
    """Integrate dln p/dT = h_fg(T)/(R_v T^2) on a 0.01 K grid, anchored at T0, P0."""
    Tg = np.linspace(273.15, 373.95, 10081)  # step 0.01 K
    hfg = np.array([sat_if97(float(T))["hfg"] for T in Tg])
    f = hfg / (R_V * Tg ** 2)
    F = cumulative_trapezoid(f, Tg, initial=0.0)
    F0 = float(np.interp(T0, Tg, F))
    lnp = math.log(P0) + (F - F0)
    return Tg, lnp


def make_route_td(Tg: np.ndarray, lnp: np.ndarray):
    def p_route(T: float) -> float:
        return math.exp(float(np.interp(T, Tg, lnp)))
    return p_route


# ---- route 3: Antoine ---------------------------------------------------------------
def antoine_P(T: float, A: float, B: float, C: float) -> float:
    return 10.0 ** (A - B / (T + C))


def make_route_antoine(A: float, B: float, C: float):
    def p_route(T: float) -> float:
        return antoine_P(T, A, B, C)
    return p_route


def fit_antoine(T_lo: float, T_hi: float, n: int, label: str) -> dict:
    """Fit log10(Ps) = A - B/(T+C) on n evenly spaced reference temperatures."""
    T = np.linspace(T_lo, T_hi, n)
    logp = np.array([math.log10(ps_ref(float(t))) for t in T])

    def resid(x: np.ndarray) -> np.ndarray:
        return x[0] - x[1] / (T + x[2]) - logp

    fit = least_squares(
        resid, x0=np.array(ANTOINE_P0, dtype=float),
        xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=20000,
    )
    # convergence check: refit from the solution, the cost must not change beyond 1e-10
    refit = least_squares(
        resid, x0=fit.x, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=20000,
    )
    cost_change = abs(float(refit.cost) - float(fit.cost))
    param_change = float(np.max(np.abs(refit.x - fit.x)))
    converged = bool(fit.success and refit.success and cost_change < 1e-10)
    rms_log = float(np.sqrt(np.mean(fit.fun ** 2)))
    logger.info(
        f"Antoine fit [{label}] n={n} status={fit.status} success={fit.success} "
        f"A={fit.x[0]:.6f} B={fit.x[1]:.4f} C={fit.x[2]:.4f} "
        f"rms_log10={rms_log:.3e} cost_change_refit={cost_change:.2e} "
        f"param_change_refit={param_change:.2e} converged={converged}"
    )
    return {
        "A": float(fit.x[0]), "B": float(fit.x[1]), "C": float(fit.x[2]),
        "n_points": int(n), "T_range_K": [float(T_lo), float(T_hi)],
        "status": int(fit.status), "success": bool(fit.success),
        "nfev": int(fit.nfev), "cost": float(fit.cost),
        "cost_change_on_refit": cost_change, "param_change_on_refit": param_change,
        "converged": converged, "rms_log10_residual": rms_log,
    }


# ---- metrics -------------------------------------------------------------------------
def err_stats(e: np.ndarray, h: np.ndarray, mask: np.ndarray) -> dict:
    ee = e[mask]
    hh = h[mask]
    if ee.size == 0:
        return {"n": 0}
    i = int(np.argmax(np.abs(ee)))
    last = int(np.argmax(h))
    return {
        "n": int(mask.sum()),
        "rms_K": float(np.sqrt(np.mean(ee ** 2))),
        "max_abs_K": float(np.abs(ee).max()),
        "altitude_of_max_m": float(hh[i]),
        "bias_K": float(np.mean(ee)),
        "err_at_4000m_K": float(e[last]),
    }


def dpdt(fn, T: float, lo: float, hi: float, h: float = DT_DIFF) -> float:
    """Central difference for dPs/dT; one-sided at the ends of the valid range."""
    if T - h < lo:
        return (fn(T + h) - fn(T)) / h
    if T + h > hi:
        return (fn(T) - fn(T - h)) / h
    return (fn(T + h) - fn(T - h)) / (2.0 * h)


def p95(T: float) -> float:
    return IAPWS95(T=T, x=0).P * 1e6


def clap_point(T: float, A: float, B: float, C: float) -> dict:
    """Clapeyron residuals r = (dPs/dT) T Dv / L - 1 at saturation temperature T."""
    Ps = ps_ref(T)
    dPdT = dpdt(ps_ref, T, T_TRIPLE, T_CRIT)
    s = sat_if97(T)
    L = s["hfg"]
    Zv = Ps / (s["rho_v"] * R_V * T)
    Dv_A = R_V * T / Ps                  # ideal vapour
    Dv_B = Zv * R_V * T / Ps             # real-vapour factor Z_v
    Dv_C = 1.0 / s["rho_v"] - 1.0 / s["rho_l"]   # Z_v plus liquid term
    rA = dPdT * T * Dv_A / L - 1.0
    rB = dPdT * T * Dv_B / L - 1.0
    rC = dPdT * T * Dv_C / L - 1.0

    # independent curve 1: Antoine derivative, dP/dT = P ln10 B/(T+C)^2
    P_ant = antoine_P(T, A, B, C)
    dPdT_ant = P_ant * math.log(10.0) * B / (T + C) ** 2
    rB_ant = dPdT_ant * T * Dv_B / L - 1.0

    # independent curve 2: IAPWS-95 saturation (its own P, L, rho, Z_v, dP/dT)
    v95 = IAPWS95(T=T, x=1)
    l95 = IAPWS95(T=T, x=0)
    P95 = v95.P * 1e6
    L95 = (v95.h - l95.h) * 1e3
    dPdT95 = dpdt(p95, T, T_TRIPLE, T_CRIT)
    Zv95 = P95 / (v95.rho * R_V * T)
    Dv95_B = Zv95 * R_V * T / P95
    rB_95 = dPdT95 * T * Dv95_B / L95 - 1.0
    Dv95_C = 1.0 / v95.rho - 1.0 / l95.rho
    rC_95 = dPdT95 * T * Dv95_C / L95 - 1.0

    return {
        "T_K": T, "Ps_Pa": Ps, "dPsdT_IF97_Pa_per_K": dPdT, "hfg_IF97_J_per_kg": L,
        "rho_v_IF97": s["rho_v"], "rho_l_IF97": s["rho_l"], "Zv_IF97": Zv,
        "rA_ideal_vapour": rA, "rB_Zv_corrected": rB, "rC_Zv_plus_liquid": rC,
        "dPsdT_Antoine_Pa_per_K": dPdT_ant, "rB_Antoine_derivative": rB_ant,
        "dPsdT_IAPWS95_Pa_per_K": dPdT95, "hfg_IAPWS95_J_per_kg": L95,
        "Zv_IAPWS95": Zv95, "rB_IAPWS95_derivative": rB_95, "rC_IAPWS95_derivative": rC_95,
    }


@logger.catch(reraise=True)
def main() -> None:
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (3600, 3600))
    except (ValueError, OSError) as exc:
        logger.warning(f"Could not set CPU-time limit: {exc}")

    t_start = time.time()
    logger.info("=== Held-out test of vapour-pressure routes + Clapeyron check ===")

    # ---- Step 1: sanity checks ---------------------------------------------------
    sanity = {}
    tb_sea = invert_T(ps_ref, P0)
    sanity["Tb_ref_sea_level_K"] = tb_sea
    sanity["Tb_ref_sea_level_ok"] = bool(abs(tb_sea - 373.124) <= 0.01)
    tp = ps_ref(T_TRIPLE)
    sanity["Ps_triple_Pa"] = tp
    sanity["Ps_triple_ok"] = bool(abs(tp - 611.657) <= 0.01)
    p4000 = p_std(4000.0)
    sanity["p_std_4000m_Pa"] = p4000
    sanity["p_std_4000m_ok"] = bool(abs(p4000 - 61640.0) <= 20.0)
    zv373 = sat_if97(373.15)
    Zv373 = ps_ref(373.15) / (zv373["rho_v"] * R_V * 373.15)
    sanity["Zv_373_15K"] = Zv373
    sanity["Zv_373_15K_ok"] = bool(0.97 <= Zv373 <= 0.99)
    sanity["all_ok"] = bool(
        sanity["Tb_ref_sea_level_ok"] and sanity["Ps_triple_ok"]
        and sanity["p_std_4000m_ok"] and sanity["Zv_373_15K_ok"]
    )
    logger.info(f"Sanity: {json.dumps(sanity, default=float)}")
    if not sanity["all_ok"]:
        logger.error("Step 1 sanity checks failed; see summary. Stopping.")
        raise SystemExit(2)

    # ---- Step 2: build routes ------------------------------------------------------
    L_const = sat_if97(T0)["hfg"]
    logger.info(f"Constant latent heat at {T0} K: L = {L_const:.1f} J/kg")
    p_const = make_route_const(L_const)

    logger.info("Building temperature-dependent-L table (0.01 K grid, IF97)")
    t_tab = time.time()
    Tg, lnp_tab = build_td_table()
    logger.info(f"TD-L table built in {time.time() - t_tab:.1f} s, {Tg.size} points")
    p_td = make_route_td(Tg, lnp_tab)

    # Antoine: fitted on the in-sample range (main) and the sensitivity range
    ant_main = fit_antoine(FIT_LO, FIT_HI, 91, "273.15-363.15 K, 1 K steps")
    ant_sens = fit_antoine(FIT_LO, SENS_FIT_HI, 81, "273.15-353.15 K, 1 K steps (sensitivity)")
    p_ant = make_route_antoine(ant_main["A"], ant_main["B"], ant_main["C"])
    p_ant_sens = make_route_antoine(ant_sens["A"], ant_sens["B"], ant_sens["C"])

    # ---- Step 3: grid inversions ---------------------------------------------------
    p_grid = np.array([p_std(h) for h in GRID_H])
    tb_ref = np.array([invert_T(ps_ref, p) for p in p_grid])
    tb_const = np.array([invert_T(p_const, p) for p in p_grid])
    tb_td = np.array([invert_T(p_td, p) for p in p_grid])
    tb_ant = np.array([invert_T(p_ant, p) for p in p_grid])
    tb_ant_sens = np.array([invert_T(p_ant_sens, p) for p in p_grid])

    # analytic cross-check of the constant-L inversion (bisection vs closed form)
    tb_const_analytic = np.array(
        [1.0 / (1.0 / T0 - math.log(p / P0) * R_V / L_const) for p in p_grid]
    )
    analytic_gap = float(np.max(np.abs(tb_const - tb_const_analytic)))
    logger.info(f"Constant-L bisection vs closed form: max gap {analytic_gap:.2e} K")

    e_const = tb_const - tb_ref
    e_td = tb_td - tb_ref
    e_ant = tb_ant - tb_ref
    e_ant_sens = tb_ant_sens - tb_ref

    in_sample = (tb_ref >= FIT_LO) & (tb_ref < FIT_HI)
    held_out = (tb_ref >= HELD_LO) & (tb_ref <= HELD_HI)
    full = np.ones_like(tb_ref, dtype=bool)
    held_sens = (tb_ref >= SENS_HELD_LO) & (tb_ref <= HELD_HI)
    band = np.where(in_sample, "in_sample", "held_out")
    logger.info(
        f"Grid: 81 points; in_sample={int(in_sample.sum())}, held_out={int(held_out.sum())} "
        f"(Tb_ref 363.15-373.15 K), held_out altitude range "
        f"{GRID_H[held_out].min():.0f}-{GRID_H[held_out].max():.0f} m"
    )

    routes = {
        "constant_L_clausius_clapeyron": e_const,
        "td_L_clausius_clapeyron": e_td,
        "antoine": e_ant,
    }
    route_stats = {}
    for name, e in routes.items():
        route_stats[name] = {
            "full_grid": err_stats(e, GRID_H, full),
            "in_sample_tagged": err_stats(e, GRID_H, in_sample),
            "held_out": err_stats(e, GRID_H, held_out),
        }
        logger.info(
            f"{name}: full max={route_stats[name]['full_grid']['max_abs_K']:.4f} K "
            f"rms={route_stats[name]['full_grid']['rms_K']:.4f} K | "
            f"held-out rms={route_stats[name]['held_out']['rms_K']:.5f} K "
            f"max={route_stats[name]['held_out']['max_abs_K']:.5f} K"
        )
    route_stats["antoine"]["fit_range_inversion_residual"] = err_stats(e_ant, GRID_H, in_sample)

    sens_stats = {
        "fit_range_K": [FIT_LO, SENS_FIT_HI],
        "held_out_range_K": [SENS_HELD_LO, HELD_HI],
        "antoine_params": {k: ant_sens[k] for k in ("A", "B", "C")},
        "held_out": err_stats(e_ant_sens, GRID_H, held_sens),
        "not_ranked": True,
    }
    logger.info(
        f"Sensitivity (Antoine fit 273.15-353.15 K): held-out [353.15,373.15] n={sens_stats['held_out']['n']} "
        f"rms={sens_stats['held_out']['rms_K']:.5f} K max={sens_stats['held_out']['max_abs_K']:.5f} K"
    )

    # ---- Step 4: regression against prior numbers ----------------------------------------
    fg = {n: route_stats[n]["full_grid"] for n in routes}
    regression = {
        "constant_L_max_K": {"expected": REG_TARGETS["constant_L_max_K"], "got": fg["constant_L_clausius_clapeyron"]["max_abs_K"], "tol": REG_TOL_K},
        "constant_L_rms_K": {"expected": REG_TARGETS["constant_L_rms_K"], "got": fg["constant_L_clausius_clapeyron"]["rms_K"], "tol": REG_TOL_K},
        "td_L_max_K": {"expected": REG_TARGETS["td_L_max_K"], "got": fg["td_L_clausius_clapeyron"]["max_abs_K"], "tol": REG_TOL_K},
        "td_L_rms_K": {"expected": REG_TARGETS["td_L_rms_K"], "got": fg["td_L_clausius_clapeyron"]["rms_K"], "tol": REG_TOL_K},
        "antoine_in_sample_max_K": {"expected": REG_TARGETS["antoine_in_sample_max_K"], "got": route_stats["antoine"]["in_sample_tagged"]["max_abs_K"], "tol": REG_TOL_K},
        "antoine_in_sample_rms_K": {"expected": REG_TARGETS["antoine_in_sample_rms_K"], "got": route_stats["antoine"]["in_sample_tagged"]["rms_K"], "tol": REG_TOL_K},
    }
    for k, v in regression.items():
        v["pass"] = bool(abs(v["got"] - v["expected"]) <= v["tol"])
        logger.info(f"Regression {k}: expected {v['expected']} got {v['got']:.5f} pass={v['pass']}")

    # ---- Step 5: ranking ----------------------------------------------------------------
    ranking_rows = []
    for name in routes:
        fgs = route_stats[name]["full_grid"]
        survives = fgs["max_abs_K"] <= SURVIVAL_MAX_K
        ranking_rows.append({
            "route": name,
            "held_out_rms_K": route_stats[name]["held_out"]["rms_K"],
            "full_grid_max_abs_K": fgs["max_abs_K"],
            "survives_0_6K_rule": bool(survives),
        })
    survivors = [r for r in ranking_rows if r["survives_0_6K_rule"]]
    survivors.sort(key=lambda r: r["held_out_rms_K"])
    ranking = [
        {"rank": i + 1, **r} for i, r in enumerate(survivors)
    ]
    logger.info(f"Ranking (survivors, by held-out RMS): {[r['route'] for r in ranking]}")

    # ---- Step 6: Clapeyron check -------------------------------------------------------
    t_clap = time.time()
    grid_T_clap = sorted(float(t) for t in tb_ref[(tb_ref >= 356.0) & (tb_ref <= 373.15)])
    # IAPWS-95 rejects T = 273.15 K (valid from 273.16 K), so the sweep starts at the triple point
    sweep_T = [float(t) for t in np.linspace(T_TRIPLE, 373.15, 101)]
    logger.info(f"Clapeyron: {len(grid_T_clap)} grid saturation temperatures (356-373 K), "
                f"{len(sweep_T)} sweep points (273.15-373.15 K)")
    clap_grid = [clap_point(T, ant_main["A"], ant_main["B"], ant_main["C"]) for T in grid_T_clap]
    clap_sweep = [clap_point(T, ant_main["A"], ant_main["B"], ant_main["C"]) for T in sweep_T]
    clap_all = clap_grid + clap_sweep
    logger.info(f"Clapeyron points computed in {time.time() - t_clap:.1f} s")

    def max_abs(key: str) -> float:
        return float(max(abs(p[key]) for p in clap_all))

    max_rA = max_abs("rA_ideal_vapour")
    max_rB = max_abs("rB_Zv_corrected")
    max_rC = max_abs("rC_Zv_plus_liquid")
    max_rB_ant = max_abs("rB_Antoine_derivative")
    max_rB_95 = max_abs("rB_IAPWS95_derivative")
    max_rC_95 = max_abs("rC_IAPWS95_derivative")
    identity_pass = max_rB <= CL_TOL
    indep_pass = max(max_rB_ant, max_rB_95) <= CL_TOL
    if identity_pass and indep_pass:
        verdict = "holds (largely an identity; the independent-curve residuals also pass)"
    elif indep_pass:
        verdict = "partly holds (only the independent-curve residuals pass)"
    else:
        verdict = "fails"
    clap_summary = {
        "n_points_grid_T_356_373K": len(clap_grid),
        "n_points_sweep_273_373K": len(clap_sweep),
        "max_abs_rA_ideal_vapour": max_rA,
        "max_abs_rB_Zv_corrected": max_rB,
        "max_abs_rC_Zv_plus_liquid": max_rC,
        "max_abs_rB_Antoine_derivative": max_rB_ant,
        "max_abs_rB_IAPWS95_derivative": max_rB_95,
        "max_abs_rC_IAPWS95_derivative": max_rC_95,
        "rA_minus_rB_max_abs": max_rA - max_rB,
        "rA_exceeds_1pct_tolerance": bool(max_rA > CL_TOL),
        "identity_pass_Zv_corrected_IF97": bool(identity_pass),
        "independent_curve_pass": bool(indep_pass),
        "verdict": verdict,
        "identity_caveat": (
            "dP/dT, L and Z_v come from the same IF97 equations, and Dv_B = 1/rho_v "
            "exactly, so the Z_v-corrected IF97 residual is near zero by construction. "
            "The independent-curve residuals (Antoine and IAPWS-95 derivatives) carry "
            "the test."
        ),
        "tolerance_relative": CL_TOL,
    }
    logger.info(f"Clapeyron: max|rA|={max_rA:.5f} max|rB|={max_rB:.2e} "
                f"max|rB_ant|={max_rB_ant:.5f} max|rB_95|={max_rB_95:.5f} verdict: {verdict}")

    # ---- Step 7: dataset cross-check --------------------------------------------------
    cross = {"file": "data/full_data_out.json", "status": "not run"}
    try:
        dat = json.loads(DATASET_FILE.read_text())
        rows = dat["datasets"][0]["examples"]
        diffs = []
        for row in rows:
            h = float(json.loads(row["input"])["elevation_m"])
            t_tab_k = float(row["output"]) + 273.15
            t_ref_k = invert_T(ps_ref, p_std(h))
            diffs.append({"elevation_m": h, "dataset_K": t_tab_k, "ref_K": t_ref_k,
                          "ref_minus_dataset_K": t_ref_k - t_tab_k})
        arr = np.array([d["ref_minus_dataset_K"] for d in diffs])
        cross = {
            "file": "data/full_data_out.json",
            "status": "ok",
            "n_rows": len(diffs),
            "dataset_unit_note": "dataset output is in degrees C (metadata_formula_boiling_C column); converted +273.15 to K",
            "max_abs_diff_K": float(np.max(np.abs(arr))),
            "mean_diff_K": float(np.mean(arr)),
            "rows": diffs,
            "interpretation": "consistency between two reference calculations, not validity against measurements",
        }
        logger.info(f"Dataset cross-check: n={len(diffs)} max|diff|={cross['max_abs_diff_K']:.4f} K "
                    f"mean={cross['mean_diff_K']:.4f} K")
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        logger.error(f"Dataset cross-check failed: {exc}")
        cross = {"file": "data/full_data_out.json", "status": f"failed: {exc}"}

    # ---- Step 8: write outputs --------------------------------------------------------------
    grid_csv = RES_DIR / "grid_values.csv"
    with grid_csv.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["elevation_m", "p_std_Pa", "Tb_ref_K", "Tb_constant_L_K", "Tb_td_L_K",
                    "Tb_antoine_K", "err_constant_L_K", "err_td_L_K", "err_antoine_K",
                    "err_antoine_sensitivity_K", "tag"])
        for i in range(GRID_H.size):
            w.writerow([f"{GRID_H[i]:.0f}", f"{p_grid[i]:.4f}", f"{tb_ref[i]:.9f}",
                        f"{tb_const[i]:.9f}", f"{tb_td[i]:.9f}", f"{tb_ant[i]:.9f}",
                        f"{e_const[i]:.9f}", f"{e_td[i]:.9f}", f"{e_ant[i]:.9f}",
                        f"{e_ant_sens[i]:.9f}", band[i]])
    logger.info(f"Wrote {_rel(grid_csv)}")

    clap_path = RES_DIR / "clapeyron.json"
    clap_path.write_text(json.dumps({
        "method": "Clapeyron residual r = (dPs/dT) T Dv / L - 1",
        "dPdT_step_K": DT_DIFF,
        "routes": {"A": "ideal vapour Dv = R_v T / Ps", "B": "Z_v corrected Dv = Z_v R_v T / Ps",
                   "C": "Z_v plus liquid Dv = 1/rho_v - 1/rho_l"},
        "summary": clap_summary,
        "points": clap_all,
    }, indent=2))
    logger.info(f"Wrote {_rel(clap_path)}")

    summary = {
        "title": "Held-out test of vapour-pressure routes and Clapeyron check",
        "reference": "IAPWS-IF97 region 4 (iapws 1.5.5), saturation pressure",
        "atmosphere": "U.S. Standard Atmosphere 1976 troposphere pressure, 0-4000 m, 50 m steps (81 points)",
        "antoine_fit_main": ant_main,
        "antoine_fit_sensitivity": ant_sens,
        "sanity_checks": sanity,
        "regression_against_prior_screen": regression,
        "regression_all_pass": bool(all(v["pass"] for v in regression.values())),
        "grid_counts": {"in_sample_tagged": int(in_sample.sum()), "held_out": int(held_out.sum()),
                        "full": int(full.sum())},
        "route_errors": route_stats,
        "sensitivity_antoine_273_353_fit": sens_stats,
        "ranking_held_out_rms_survivors": ranking,
        "all_routes_survival": ranking_rows,
        "constant_L_bisection_vs_closed_form_max_gap_K": analytic_gap,
        "clapeyron": clap_summary,
        "interpretation_status": (
            "PROVISIONAL: the Antoine regression target (0.0042 K in-sample) did not reproduce; "
            "the executed value is reported, and rankings and verdicts are not interpreted until it is resolved."
            if not all(v["pass"] for v in regression.values()) else "regression targets reproduced"
        ),
        "dataset_cross_check": {k: v for k, v in cross.items() if k != "rows"},
        "runtime_s": time.time() - t_start,
        "provenance": {
            "fallback_used": "none (iapws package used as reference)",
            "measured_data_used": False,
        },
    }
    summary_path = RES_DIR / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    logger.info(f"Wrote {_rel(summary_path)}")

    method_out = {
        "metadata": {
            "method_name": "Vapour-pressure routes for water boiling temperature vs altitude",
            "description": "Model-to-reference comparison against IAPWS-IF97 saturation; one example per 50 m altitude.",
            "reference": "IAPWS-IF97 region 4 (iapws package)",
            "units": {"output": "boiling temperature, K", "predict_*": "boiling temperature, K"},
            "routes": ["constant_L_clausius_clapeyron", "td_L_clausius_clapeyron", "antoine"],
            "antoine_fit_range_K": [FIT_LO, FIT_HI],
            "held_out_range_K": [HELD_LO, HELD_HI],
            "runtime_s": time.time() - t_start,
        },
        "datasets": [{
            "dataset": "altitude_grid_0_4000m_50m_IF97_reference",
            "examples": [],
        }],
    }
    examples = method_out["datasets"][0]["examples"]
    for i in range(GRID_H.size):
        examples.append({
            "input": json.dumps({"elevation_m": float(GRID_H[i])}),
            "output": f"{tb_ref[i]:.6f}",
            "metadata_p_std_Pa": f"{p_grid[i]:.4f}",
            "metadata_split": str(band[i]),
            "metadata_err_constant_L_K": f"{e_const[i]:.6f}",
            "metadata_err_td_L_K": f"{e_td[i]:.6f}",
            "metadata_err_antoine_K": f"{e_ant[i]:.6f}",
            "predict_constant_L_clausius_clapeyron": f"{tb_const[i]:.6f}",
            "predict_td_L_clausius_clapeyron": f"{tb_td[i]:.6f}",
            "predict_antoine": f"{tb_ant[i]:.6f}",
        })
    out_path = WS / "method_out.json"
    out_path.write_text(json.dumps(method_out, indent=2))
    full_path = WS / "full_method_out.json"
    full_path.write_text(json.dumps(method_out, indent=2))
    logger.info(f"Wrote {_rel(full_path)} (full, {len(examples)} examples)")
    logger.info(f"Wrote {_rel(out_path)} with {len(examples)} examples")

    logger.info(f"Done in {time.time() - t_start:.1f} s")


if __name__ == "__main__":
    main()
