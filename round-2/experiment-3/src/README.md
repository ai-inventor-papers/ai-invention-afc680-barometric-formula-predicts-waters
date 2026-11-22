# Testing barometric boiling-point formulas against measured records

## Result (read first)

No verified measured boiling-point record with site elevation, station pressure,
observed boiling temperature and stated instrument uncertainties was found in this
run's search. The accepted set is therefore empty (0 sites; the minimum for the test
is 15). **All three claims are UNDERPOWERED and untested.** The pipeline runs fully;
its statistics are reported as empty, and no residuals are pooled from equation-derived
tables.

What was verified in this run:

- Explicit Wagner-Pruss (IAPWS-95) saturation equation: normal boiling point
  (101323.9 Pa at 373.124 K, within 5 Pa of 101325 Pa), triple point (611.657 Pa),
  inverse round-trip error 3.7e-10 K, and agreement with the `iapws` 1.5.5 package
  within 2.0e-3 K at 10 temperatures.
- Model-only reference-grid structural term (isothermal minus lapse-rate boiling
  temperature, 100 m grid, 0-4000 m): 0.332 K at 3000 m and 0.588 K at 4000 m, matching
  the earlier reference screen. This is a model result, not validation.
- dTb/dp at 1 atm = 0.2765 K/kPa, consistent with the 0.28 K/kPa scale in the plan.

## Layout

- `pyproject.toml` - pinned dependency versions.
- `build_method_out.py` - builds `full_method_out.json` from `method.py` functions.
- `rederive_check.py` - independent re-derivation of the reference-grid numbers.
- `method.py` - full pipeline: constants, saturation equation and checks, site
  loading with holdout rule, residuals, bootstrap, claim tests, reference grid.
- `data/candidates.csv` - every candidate source found, with status and reason.
  All six were dropped (equation-derived, no station pressure, or unverified).
- `data/sites.json` - accepted measured sites (empty list in this run).
- `results/summary.json` - statistics, claim verdicts, underpowered flag, hashes.
- `results/residuals.csv` - not written (no accepted sites).
- `results/bootstrap.json` - bootstrap output (no sites).
- `results/reference_grid.json` - model-only structural term on the 100 m grid.
- `results/cross_check.json` - dataset-artifact cross-check, recorded as not checkable.
- `results/fig_reference_structural_spec.json` - chart spec for the figure.
- `figures/fig_reference_structural.pdf` / `.png` - model-only structural term vs
  altitude (rendered with aii-data-fig-gen).
- `logs/run.log` - run log.

## How to run

```
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python numpy pandas requests loguru iapws matplotlib
.venv/bin/python method.py
```

To run the test, add verified records to `data/sites.json` as a JSON list with fields
`id`, `source`, `elevation_m`, `station_pressure_pa`, `observed_tb_C`, and optionally
`thermometer_u_K` and `barometer_u_kPa`, then re-run. The test runs at 15 or more
verified sites.

## Limitations

- No humidity term: the record schema carries no humidity.
- The holdout rule (every third site by elevation) is fixed in code before residuals.
- The cross-check against the dataset artifact was not performed.
- The schema check (`exp_gen_sol_out`) was not applied: its input/output rows do not fit
  a run with no measured records.

## Restoring removed files

The `.venv/` directory is regenerable with:

```
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python numpy pandas requests loguru iapws matplotlib
```

`__pycache__/` (Python bytecode cache) is regenerated automatically on the next run:

```
.venv/bin/python method.py
```
