# Reproducibility

This folder is one artifact of a public GitHub repository. Clone the repository, then `cd` into this folder.
Every path below is relative to this folder.

## 1. Obtain the artifact
```
git clone <repository-url>
cd <repository>/<this-artifact-folder>
```
Inputs:
- **Dataset (published, not private):** `data/full_data_out.json`, `data/mini_data_out.json`,
  `data/preview_data_out.json` are copies of the full, mini and preview files of dependency
  `art__Ga8TbdhmlP8` (Water Boiling Temperature by Elevation Reference Table). They are included, so no
  download is needed. The cross-check reads only `full_data_out.json`.
- **User uploads:** none were provided for this artifact (the upload folder did not exist), so nothing private is needed.
- **Models, checkpoints, API keys, environment variables:** none. The run makes no network calls.

## 2. System and Python
- Python 3.12 (the executed run used CPython 3.12.10 from `uv`). Install `uv` first.
- No system packages are required beyond `uv`.
- The run that produced the results was executed on macOS (Apple silicon, arm64). Ubuntu x86_64 or arm64 should
  give the same numbers because the calculations are deterministic and pure NumPy/SciPy/iapws. This was not run on
  Ubuntu; treat the Ubuntu path as untested until someone runs it.
- Hardware: CPU only. No GPU. Memory use is small (well under 1 GB). Runtime is about 4 seconds.

## 3. Environment (exact pinned versions)
The exact versions installed in the executed environment are in `requirements.txt` and `pyproject.toml`. The
main ones are: `iapws==1.5.5`, `numpy==2.5.5`, `scipy==1.18.1`, `loguru==0.8.0`, `psutil==7.2.2`,
`matplotlib==3.11.2`, `jsonschema==4.26.0`.
```
./restore.sh          # uv venv .venv --python=3.12 ; uv pip install -r requirements.txt
```
(`restore.sh` was run and tested in this workspace; it installs the same pinned set.)

## 4. Commands, in order
All commands are run from this folder.
1. `uv run method.py`
   - Writes `results/summary.json`, `results/grid_values.csv`, `results/clapeyron.json`, `method_out.json`.
   - Logs go to `logs/run.log`. Runtime is about 4 s.
   - No seeds: there is no sampling. Results are deterministic.
2. `uv run make_mini_preview.py`
   - Writes `mini_method_out.json` (first 3 examples) and `preview_method_out.json`
     (the same, with strings cut to 200 characters).
   - `full_method_out.json` is a byte copy of `method_out.json` (made with `cp`).
3. `uv run make_fig_spec.py`
   - Writes `figures/fig_error_vs_altitude_spec.json` from `results/grid_values.csv`.
4. Render the figure with the `aii-data-fig-gen` generator:
   `python <aii-data-fig-gen>/scripts/chart_gen.py --spec figures/fig_error_vs_altitude_spec.json --out figures/fig_error_vs_altitude`
   This writes `figures/fig_error_vs_altitude.pdf` and `.png`. The generator is a skill of the AI Inventor
   pipeline, not part of this repository.
5. `uv run diag/antoine_diag.py > logs/antoine_diag_output.txt` reproduces the Antoine fit diagnostic.
6. `uv run audit/rederive.py` independently recomputes the headline numbers from the raw CSV and JSON
   (see Section 6) and writes `audit/rederive_out.json`.

Configuration is fixed in `method.py` (no config file): pressure grid 0-4000 m in 50 m steps; reference IAPWS-IF97
region 4; Antoine start values A = 10.19625, B = 1730.63, C = -39.724; fit range 273.15-363.15 K (1 K steps);
held-out band 363.15-373.15 K; sensitivity fit 273.15-353.15 K; Clapeyron step 0.01 K.

## 5. What a reader should get, and where it appears
| Output | Contents |
|---|---|
| `results/summary.json` | every number quoted in the README; regression checks; sanity checks; ranking; Clapeyron verdict |
| `results/grid_values.csv` | boiling temperatures and errors for all routes at 81 altitudes, tagged in-sample or held-out |
| `results/clapeyron.json` | per-point Clapeyron residuals (routes A, B, C; Antoine and IAPWS-95 derivatives) |
| `method_out.json` | exp_gen_sol_out-format output, 81 examples (full) |
| `figures/fig_error_vs_altitude.pdf` | error against altitude for the three routes |
| `audit/rederive_out.json` | independent re-derivation results |

Expected numbers (executed, `results/summary.json`):
- Constant-L Clausius-Clapeyron: full-grid max 0.27982 K at 4000 m; RMS 0.15324 K.
- Temperature-dependent-L: full-grid max 0.17649 K; RMS 0.10773 K.
- Antoine (fit 273.15-363.15 K): full-grid max 0.08562 K at 0 m; in-sample max 0.03576 K at 3000 m (RMS 0.02958 K).
- Held-out band (60 grid points, 0-2950 m): RMS 0.10778 K (constant-L), 0.08279 K (TD-L), 0.06126 K (Antoine).
- Clapeyron: max |r_A| (ideal vapour) 1.626 %; max |r_B| (Z_v-corrected) 0.061 %; independent-curve max |r| 0.92 % (Antoine) and 0.062 % (IAPWS-95).

**Known mismatch (unresolved):** the prior screen's Antoine in-sample target (max 0.0042 K, RMS 0.0022 K) does
not reproduce; this run gives 0.0358 K and 0.0296 K. `logs/antoine_diag_output.txt` shows that both a
log-space and a linear-pressure fit give the same behaviour, so this is not a code error. Rankings that depend
on Antoine are provisional until this is resolved.

## 6. Independent re-derivation (audit)
`audit/rederive.py` recomputes, through code paths other than `method.py`:
- route errors from the raw columns of `results/grid_values.csv`;
- the reference boiling temperatures with `scipy.optimize.brentq` (not bisection): max gap to the stored values 8.06e-10 K;
- Clapeyron residuals from the raw per-point fields in `results/clapeyron.json`.

It matched every headline number in `results/summary.json` (route maxima and held-out RMS to 5 decimals,
Clapeyron max |r_A| 0.016261 and max |r_B| 0.000610). The ranking by held-out RMS is Antoine, then TD-L,
then constant-L.

Not done: a placebo or shuffled-input control. No statistical significance test is computed here; the
ranking is a direct comparison of error metrics, so a permutation control does not apply.

## 7. Limits to keep in mind
- Model-to-reference only. No measured boiling records are used.
- The held-out band is a temperature extrapolation adjacent to the fit range (0-2950 m), not a separate site holdout.
- The Clapeyron Z_v-corrected residual is an identity; the independent-curve residuals carry the test.
- The dataset's `output` field is in °C; the cross-check converts it with +273.15 K.
