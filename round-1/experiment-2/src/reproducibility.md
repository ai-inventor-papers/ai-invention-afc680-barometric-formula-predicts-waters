# Reproducibility: screening vapour-pressure shortcuts for water boiling temperature

## 1. Getting the artifact
This folder is published as one folder of a public GitHub repository. Clone the repository, then `cd` into this folder
(the folder that contains `method.py` and `pyproject.toml`). All paths below are relative to this folder.

## 2. Environment
- Python 3.13 (3.13.3 was used; `requires-python = ">=3.13"`).
- No system packages are needed beyond a Python 3.13 interpreter and `uv`.
- Create the environment and install the exact versions used (these match `pyproject.toml`):
```
uv venv .venv
VIRTUAL_ENV=$PWD/.venv uv pip install iapws==1.5.5 numpy==2.5.5 scipy==1.18.1
```
- Pinned versions: `iapws` 1.5.5, `numpy` 2.5.5, `scipy` 1.18.1.
- No GPU, no torch, no network access is needed at run time. No API keys or environment variables are needed.

## 3. Data, models and downloads
- No dataset, model checkpoint or download is used. Every input is a closed-form equation or a table computed by the code:
  the IAPWS-IF97 saturation equation (region 4, through the `iapws` package), the U.S. Standard Atmosphere 1976 troposphere formula,
  and the NIST WebBook water constants (typed in `method.py`).
- The reference enthalpies for latent heat come from the same `iapws` package (`IAPWS97`, x = 0 and x = 1).
- The user uploads folder was not used, so no private copy is needed.

## 4. Commands, in order
Hardware: CPU only (cpu_basic pod, 2 shared vCPUs, 16 GB). Full run about 1 s; dry run about 7 s including import.
```
.venv/bin/python method.py --dry     # five altitudes (0, 1000, 2000, 3000, 4000 m), prints the four temperatures and errors
.venv/bin/python method.py           # full run, 81 altitudes (0-4000 m, 50 m steps); writes results/*
.venv/bin/python rederive_headlines.py   # independent re-derivation of headline numbers (pure Python + IAPWS-95)
```
The full-run console output is saved in `results/run_log.txt`.

The JSON files follow the exp_gen_sol_out schema (one dataset, 81 examples; mini and preview hold the first 3).
rows per method; preview = mini with every string truncated to 200 characters.

## 5. Expected outputs and where the numbers appear
- `method_out.json` (root; exp_gen_sol_out format) and `results/method_grid.json` (raw per-altitude grid): per-method grid (h, p_std, T_ref, T_m, e) and metrics for 81 altitudes. The three variants are
  `full_method_out.json`, `mini_method_out.json` and `preview_method_out.json`.
- `results/summary.md`: metrics table, ranking, survival verdict and check status.
- `results/antoine_fit.json`: fitted A = 7.125207, B = 1689.0362, C = 229.9526 (kPa form), residual RMS 6.006 Pa.
- `results/reference_checks.json`: checks 1 to 6. Check 3 (Clapeyron consistency at 1 %) fails: max deviation 1.59 %,
  which follows the ideal-vapour factor 1/Z_v - 1. This is reported, not corrected.
- `results/lv_table.json`: Lv(T) from IF97 enthalpies, grid mean 42.89 kJ/mol.
- `results/rederivation.json`: independent re-derivation. Headline metrics reproduce to four decimals. The reference
  temperatures from IAPWS-95 differ from IF97 by at most 0.0002 K at the tested altitudes.

Headline numbers (max |error| and RMS, K, over 0-4000 m): constant-latent-heat Clausius-Clapeyron 0.278 and 0.152;
temperature-dependent-latent-heat Clausius-Clapeyron 0.177 and 0.108; Antoine 0.0042 and 0.0022. The ranking among
survivors of the 0.6 K rule is Antoine, then temperature-dependent latent heat, then constant latent heat.

## 6. Limitations
- No published boiling-point measurements are used; the comparison is against the IAPWS reference only.
- The IF97 region 4 coefficients come from the `iapws` implementation, not from a typed copy of the release text.
