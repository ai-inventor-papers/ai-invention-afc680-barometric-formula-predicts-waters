"""Independent re-derivation of headline numbers.

Uses pure-Python arithmetic (math module, no numpy/scipy) and a different reference equation
(IAPWS-95 via the iapws package's IAPWS95 class) so the check does not repeat the code path of method.py.
Reads only results/full_method_out.json grid values to recompute the metrics, and recomputes
T_a, T_c analytically from the altitude.
"""
import json
import math
from pathlib import Path

from iapws import IAPWS95

ROOT = Path(__file__).resolve().parent
d = json.loads((ROOT / "results" / "method_grid.json").read_text())
R, g, M, T0, p0, L = 8.314462618, 9.80665, 0.0289644, 288.15, 101325.0, 0.0065
EXP = g * M / (R * L)
Ta, pa, Lv = 373.124, 101325.0, 40.66e3
A, B, C = (json.loads((ROOT / "results" / "antoine_fit.json").read_text())[k] for k in ("A", "B", "C"))

def psat95(T):
    return float(IAPWS95(T=T, x=0).P) * 1e6  # MPa -> Pa

def tref95(p):
    lo, hi = 273.16, 373.946
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if psat95(mid) > p:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

out = {}
# 1) metrics recomputed in pure Python from the stored grid
for name, m in d["methods"].items():
    errs = [(row["h_m"], row["T_m_K"] - row["T_ref_K"]) for row in m["grid"]]
    mx_h, mx = max(errs, key=lambda t: abs(t[1]))
    rms = math.sqrt(sum(e * e for _, e in errs) / len(errs))
    bias = sum(e for _, e in errs) / len(errs)
    e4000 = [e for h, e in errs if h == 4000.0][0]
    out[name] = dict(max_abs=abs(mx), rms=rms, alt_max=mx_h, bias=bias, e4000=e4000, n=len(errs),
                     stored=m["metrics"])
# 2) analytic T_a and T_c at 0, 2000, 4000 m, and T_ref from IAPWS-95 (different equation of state)
checks = []
for h in (0.0, 2000.0, 4000.0):
    p = p0 * (1 - 0.0065 * h / T0) ** EXP
    tr95 = tref95(p)
    ta = 1 / (1 / Ta - R * math.log(p / pa) / Lv)
    tc = B / (A - math.log10(p / 1000.0)) - C + 273.15  # C is the offset in T_C = T - 273.15
    grid_row = [r for r in d["methods"]["a_constant_latent_heat"]["grid"] if r["h_m"] == h][0]
    checks.append(dict(h=h, p=p, T_ref_IF97_grid=grid_row["T_ref_K"], T_ref_IAPWS95=tr95,
                       diff_ref_K=grid_row["T_ref_K"] - tr95, T_a_recomputed=ta, T_a_grid=grid_row["T_m_K"],
                       T_c_recomputed=tc,
                       T_c_grid=[r for r in d["methods"]["c_antoine"]["grid"] if r["h_m"] == h][0]["T_m_K"]))
out["point_checks"] = checks
(ROOT / "results" / "rederivation.json").write_text(json.dumps(out, indent=1, default=float))
for k, v in out.items():
    if k != "point_checks":
        print(f"{k:42s} max|e|={v['max_abs']:.4f} RMS={v['rms']:.4f} alt={v['alt_max']:.0f} bias={v['bias']:+.4f} e4000={v['e4000']:+.4f} stored_max={v['stored']['max_abs_error_K']:.4f}")
for c in checks:
    print(c)
