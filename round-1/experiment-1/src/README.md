# Barometric boiling-point screen on a 0–4000 m grid

## What was done
Two barometric pressure forms are compared for predicting the boiling point of water with altitude:

- **Isothermal** form: `p = p0 exp(-g0 z / (R T0))`, scale height ≈ 8,435 m.
- **Standard lapse-rate** form (U.S. Standard Atmosphere 1976 troposphere): `p = p0 (1 - L z / T0)^(g0/(R L))`.

Boiling temperatures come from the Wagner–Pruss (IAPWS) vapour-pressure equation, inverted by 80-step vectorised bisection. The reference is the USSA 1976 lapse-rate pressure. The 41-point grid runs from 0 to 4,000 m in 100 m steps.

**No field measurements are used.** This is a model-to-reference screen. It does not validate the formulas against measured boiling points, and it has no weather or humidity term.

## Result (see `results/summary.json`)
- Isothermal structural term s = T_iso − T_lapse: 0.04 K (1 km), 0.15 K (2 km), 0.33 K (3 km), 0.59 K (4 km).
- Isothermal error against reference: max |err| = 0.588 K at 4,000 m; RMS = 0.269 K.
- Against the 0.6 K limit the margin is 0.012 K. The rule marks this **borderline, so no pass/fail claim is made**.
- The lapse-rate form is the reference itself, so its error is zero by construction.
- Sea-level check: T_b(101.325 kPa) = 373.124 K = 99.974 °C (IAPWS-95 value; 100 °C corresponds to about 101.42 kPa).
- Cross-check against the `iapws` package (IF97 region 4) at 0, 2 and 4 km agrees to 0.0002 K.

## Layout
- `method.py` — full experiment: physics, tests T1–T7 (stop at first failure), outputs.
- `results/grid_values.csv` — every intermediate for each altitude.
- `results/summary.json` — tests, metrics at 1–4 km, max/RMS, verdicts, caveats.
- `results/method_out.json` — predictions in the `exp_gen_sol_out` schema (validated, 41 examples).
- `results/log.txt`, `logs/run.log` — run logs.
- `.aii/manifest.yaml` — storage decisions for heavy paths.

## How to run
```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python numpy loguru iapws jsonschema
.venv/bin/python method.py
```
Runtime is about one second.

## Restoring removed files
- `.venv/` (regenerable): `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python numpy loguru iapws jsonschema`

## Notes
- The USSA 1976 node pressures (101325, 89875, 79501, 70108, 61640 Pa) were recalled from the standard table, not re-fetched in this session. The lapse-rate form reproduces them within 0.01%.
- Geopotential heights are used as the grid; geometric-versus-geopotential difference is about 2.5 m at 4 km (≈0.01 K), not corrected.
