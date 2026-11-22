# Screening vapour-pressure shortcuts for the boiling point of water

Closed-form methods for the boiling temperature of water at altitude, screened against one reference:
the IAPWS-IF97 saturation curve (region 4, via the `iapws` package 1.5.5), inverted on the same altitude grid.
Pressure at altitude comes from the U.S. Standard Atmosphere 1976 troposphere (0-4000 m, 81 points, 50 m steps).

## Methods
- (a) constant-latent-heat Clausius-Clapeyron, anchored at the normal boiling point (373.124 K, 101.325 kPa), Lv = 40.66 kJ/mol (primary).
- (b) temperature-dependent-latent-heat Clausius-Clapeyron: Lv(T) from IF97 enthalpies, integrated from the anchor (DOP853, rtol 1e-10).
- (c) Antoine equation, NIST WebBook water constants converted to kPa, refitted to the reference over 273.15-373.15 K.
- Sensitivity (not ranked): (a) with Lv set to the grid-mean latent heat.

Survival rule: max |error| <= 0.6 K. Survivors ranked by RMS error.

## Layout
- `method.py` - full pipeline: reference, atmosphere, methods, errors, checks, outputs.
- `method_out.json` (root; exp_gen_sol_out format) and `results/method_grid.json` (raw per-altitude grid) - per-method grid (h, p, T_ref, T_m, e) and metrics.
- `results/summary.md` - metrics table, ranking, survival verdict, check status.
- `results/antoine_fit.json` - fitted A, B, C and residuals.
- `results/reference_checks.json` - reference, atmosphere, Clapeyron, single-point, and Antoine checks.
- `results/lv_table.json` - Lv(T) table from IF97 enthalpies used by method (b).
- `results/run_log.txt` - console output of the full run.
- `.aii/manifest.yaml` - storage decisions.

## How to run
```
uv venv .venv && VIRTUAL_ENV=$PWD/.venv uv pip install numpy scipy iapws
.venv/bin/python method.py          # full run (about 1 s)
.venv/bin/python method.py --dry    # five-altitude dry run
```

## Limitations
- No field records or published boiling-point measurements are used; the comparison is against the reference equation only.
- The Clapeyron consistency check (3) fails at the 1 % tolerance (max 1.59 % at about 373 K). The ideal-vapour Clapeyron form
  ignores the real-vapour compressibility factor (Z_v = 0.985 at 373 K); the deviation tracks 1/Z_v - 1. This is a structural
  property of the ideal-vapour route, not a table error. It is reported, not corrected.
- The IF97 region 4 coefficients were taken from the `iapws` implementation, not typed from the release text; the Psat checks
  at the triple point and the normal boiling point pass.
- Method (a) uses 40.66 kJ/mol, which is the IF97 hv - hl at 373.124 K to within 0.02 %.

## Restoring removed files
`.venv/` (deleted after the round; regenerable):
```
uv venv .venv && VIRTUAL_ENV=$PWD/.venv uv pip install numpy scipy iapws
```

## Additional files
- `pyproject.toml`: pinned dependencies (iapws 1.5.5, numpy 2.5.5, scipy 1.18.1).
- `reproducibility.md`: step-by-step reproduction instructions.
- `rederive_headlines.py`: independent re-derivation of headline metrics (pure Python, IAPWS-95 reference); writes `results/rederivation.json`.
