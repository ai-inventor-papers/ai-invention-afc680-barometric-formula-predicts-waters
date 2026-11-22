# Reproducing this artifact

What was actually run: the environment was macOS (Darwin 25, Apple silicon, CPU only, Python 3.12.14). Reproduction on Ubuntu should give the same numbers, but was not tested there.

## 1. Get the artifact

This folder is published as one folder of a public GitHub repository. Clone the repository and `cd` into this folder.

## 2. Environment

Python 3.12. Create the environment with uv (not pip):

```
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r <(sed -n 's/^    "\(.*\)",$/\1/p' pyproject.toml)
```

Or install the exact pins from `pyproject.toml` (numpy 2.5.5, iapws 1.5.5, pandas 3.1.1, scipy 1.18.1, matplotlib 3.11.2, loguru 0.8.0 and the rest). No system packages are required. Do not install or upgrade torch; it is not used.

## 3. Data, models and keys

- No downloaded data. The accepted site set is `data/sites.json`, which is an empty list in this run. Candidate sources and drop reasons are in `data/candidates.csv`.
- Saturation coefficients are copied from Wagner and Pruss (2002), J. Phys. Chem. Ref. Data 31, 387-535, Table 2, and are written in `method.py`.
- No API keys or environment variables are needed.
- The figure was rendered with the `aii-data-fig-gen` skill (`chart_gen.py`). That skill sits outside this repository. To re-render, supply the skill's `chart_gen.py` and run it on `results/fig_reference_structural_spec.json`.
- The upload folder `user_uploads` was not used. It is private and is not published.

## 4. Commands, in order

```
.venv/bin/python method.py
.venv/bin/python rederive_check.py
```

- `method.py` runs the saturation checks, the iapws cross-check, the reference grid, and the claim tests. Seed for the bootstrap: 20260314. It runs in a few seconds on CPU. Logs go to `logs/run.log`.
- `rederive_check.py` recomputes the reference-grid numbers through a different code path (iapws `IAPWS97` psat with scipy `brentq`).
- The figure was rendered from `results/fig_reference_structural_spec.json` with `chart_gen.py --spec ... --out figures/fig_reference_structural`.
- `.venv/bin/python build_method_out.py` writes `full_method_out.json` (41 grid points, two methods: isothermal and lapse-rate predicted boiling temperatures, computed by the functions in `method.py`). `mini_method_out.json` and `preview_method_out.json` were written with the aii-json rules (first 3 examples; strings cut to 200 characters) by a short inline script. The aii-json format script refused the paths in this environment.

## 5. Expected outputs

- `results/summary.json`: `underpowered: true`, accepted sites 0, all claims UNDERPOWERED and untested, saturation checks, constants, reference-grid summary.
- `results/reference_grid.json`: structural term on a 100 m grid. At 3000 m: 0.332 K. At 4000 m: 0.588 K. Positive and increasing above 0 m. This is a model-only result and is not validation.
- `results/cross_check.json`: "could not be checked" (no dataset-artifact site list at the declared path).
- `full_method_out.json`, `mini_method_out.json`, `preview_method_out.json`: model-only reference grid, 41 examples, two methods (`predict_isothermal_barometric_Tb_C`, `predict_lapse_rate_barometric_Tb_C`). No measured observation is included, so these files support no comparison against truth.

No headline number in this run is a measured result. Nothing here is a claim about measured boiling points. The measured comparison needs at least 15 verified records in `data/sites.json`. Rerunning `method.py` after adding them is the intended extension.

## Limits

- The validator in the aii-json skill refused all paths reachable from this environment. `full_method_out.json` was checked with the `exp_gen_sol_out` schema directly through `jsonschema` (Draft 7): no errors.
- No statistical test was run, so no placebo or shuffled-input check was applicable.
