# Held-out test of vapour-pressure routes and Clapeyron check

Reference-only CPU experiment. It compares three vapour-pressure routes for the boiling
temperature of water over 0-4000 m against the IAPWS-IF97 saturation curve (region 4, via the
`iapws` package). It also tests the Clapeyron relation with two ways of computing the vapour volume.

**No measured boiling records or station pressures are used.** The question asked how the formula
compares with published measurements. This run cannot answer that: the only dataset available
(`data/full_data_out.json`) is equation-derived. Every result here is model-to-reference.

## Status: provisional
The Antoine regression target did not reproduce. The prior screen reported an in-sample max of
0.0042 K; this run gives 0.0358 K (RMS 0.0296 K vs 0.0022 K). The constant-latent-heat and
temperature-dependent-latent-heat targets do reproduce. Both log-space and linear-pressure fits of
the 3-parameter Antoine form give 0.04-0.09 K errors on this range, so this is not a bug. The
mismatch is unresolved. **Route rankings that depend on Antoine are provisional.** See
`reproducibility.md`.

## Results (executed values, `results/summary.json`)

| Route | Full grid max (K) | Full grid RMS (K) | Held-out RMS (K) | Held-out max (K) |
|---|---|---|---|---|
| Constant-L Clausius-Clapeyron | 0.280 (at 4000 m) | 0.153 | 0.108 | 0.194 |
| Temperature-dependent-L Clausius-Clapeyron | 0.176 (at 4000 m) | 0.108 | 0.083 | 0.137 |
| Antoine (fit on 273.15-363.15 K) | 0.086 (at 0 m) | 0.055 | 0.061 | 0.086 |

- Held-out band: reference boiling temperature 363.15-373.15 K, which is 0-2950 m (60 grid points).
  In-sample tag: 21 points, 3000-4000 m.
- Antoine in-sample: max 0.036 K at 3000 m, RMS 0.030 K. Error at 4000 m is -0.023 K.
- Sensitivity (Antoine fit on 273.15-353.15 K, held-out 353.15-373.15 K, not ranked):
  RMS 0.092 K, max 0.133 K.
- Survival rule (full-grid max ≤ 0.6 K): all three routes survive.
- Ranking by held-out RMS (provisional): Antoine, then temperature-dependent-L, then constant-L.
- Clapeyron check (grid 356-373 K and 273.16-373.15 K sweep):
  - Ideal-vapour residual max |r| = 1.63 %.
  - Z_v-corrected residual max |r| = 0.06 %. This is an identity; see the caveat below.
  - Independent curves: Antoine derivative 0.92 %, IAPWS-95 derivative 0.06 %.
  - Verdict: "holds (largely an identity; the independent-curve residuals also pass)".
    The Antoine-derivative residual is close to the 1 % tolerance.
- Dataset cross-check (41 rows, 0-4000 m, 100 m steps): max |difference| 0.063 K, mean -0.018 K.
  This shows consistency only.

Figure: `figures/fig_error_vs_altitude.pdf` (and `.png`) shows the boiling-temperature error against
altitude for the three routes. Its raw values are in `results/grid_values.csv`.

## Layout
- `method.py`: full experiment. Reference, three routes, held-out and sensitivity splits,
  Clapeyron check, dataset cross-check, and all outputs.
- `make_mini_preview.py`: writes the mini and preview variants of `method_out.json`.
- `make_fig_spec.py`: builds the figure spec from `results/grid_values.csv`.
- `figures/`: figure spec (`fig_error_vs_altitude_spec.json`), PDF and PNG.
- `results/summary.json`: all numbers quoted above, plus regression checks and sanity checks.
- `results/grid_values.csv`: all routes on 81 points, with band tags.
- `results/clapeyron.json`: Clapeyron residuals per point (routes A, B, C; independent curves).
- `method_out.json`: exp_gen_sol_out-format output, one example per 50 m. Mini and preview
  variants are in the same folder.
- `data/`: copies of the dependency dataset (`full_data_out.json`, `mini_`, `preview_`, `reproducibility.md`).
- `diag/antoine_diag.py`: the Antoine fit diagnostic.
- `audit/rederive.py`: independent re-derivation of the headline numbers from raw files (see `reproducibility.md`).
- `requirements.txt`: exact pinned versions (`pyproject.toml` lists the same set).
- `logs/`: run logs.
- `reproducibility.md`: environment, run order, tolerances, regression table, and limits.
- `pyproject.toml`, `restore.sh`: environment definition.

## Limits
- Held-out band is a temperature extrapolation adjacent to the fit range, not a geographically
  separate holdout.
- The Clapeyron Z_v-corrected residual is an identity, so the test rests on the independent curves.
- No uncertainty intervals: the computation is deterministic.
- The dataset's `output` field is in °C, not K as the plan states. The cross-check converts it.

## How to run
```
./restore.sh                       # only if .venv/ is missing
uv run method.py                   # ~4 s; writes results/ and logs/
uv run make_mini_preview.py
uv run make_fig_spec.py
```
Then render the figure with `aii-data-fig-gen`:
`chart_gen.py --spec figures/fig_error_vs_altitude_spec.json --out figures/fig_error_vs_altitude`.

Schema validation: the `aii-json` validator only accepts files under the project directory or
`/tmp`, and this workspace is neither, so the validator's wrapper could not run. `method_out.json`
was checked directly against `exp_gen_sol_out.json` with `jsonschema` (0 errors), and every example has
non-empty `predict_*` fields.

## Restoring removed files
The only deleted path is `.venv/`, which is regenerable.
- Command: `./restore.sh`. It runs `uv venv .venv --python=3.12` and installs the exact pinned set in
  `requirements.txt` (the same versions as `pyproject.toml`). See `reproducibility.md` for the full procedure.

Everything else is text or small (under 1 MB) and is kept in the repository.
