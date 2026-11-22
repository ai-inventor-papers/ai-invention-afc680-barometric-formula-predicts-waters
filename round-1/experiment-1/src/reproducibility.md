# Reproducing the barometric boiling-point screen

This folder is published as one folder of a public GitHub repository. Start from a clone of that repository and `cd` into this folder. Every path below is relative to this folder.

## 1. Environment
- Ubuntu (or any Linux/macOS) with Python 3.12 available. The experiment was run on macOS, Python 3.12, with `uv`.
- No GPU, no network access needed at run time (the `iapws` package is used only for a cross-check and the audit script, and it is installed from PyPI).
- Install `uv` (https://docs.astral.sh/uv/), then:

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python \
  attrs==26.1.0 iapws==1.5.5 jsonschema==4.26.0 jsonschema-specifications==2025.9.1 \
  loguru==0.8.0 numpy==2.5.5 referencing==0.37.0 rpds-py==2026.9.1 scipy==1.18.1 \
  typing-extensions==4.16.0
```

Exact pinned versions are in `pyproject.toml`. Do not use `pip`; the environment was created with `uv` only.

## 2. Data, models, keys
- No datasets, model weights or API keys are used.
- The USSA 1976 node pressures (101325, 89875, 79501, 70108, 61640 Pa) are hard-coded in `method.py` from the standard table; they are not downloaded.
- The user's uploads folder was not used.

## 3. Commands, in order
```bash
.venv/bin/python method.py          # runs tests T1-T7, writes results/ and logs/
.venv/bin/python make_variants.py   # writes full/mini/preview_method_out.json
.venv/bin/python audit_rederive.py  # independent re-derivation with the iapws package (about 10 seconds)
```
- Seeds: none (the computation is deterministic).
- Hardware: CPU only, a laptop-class machine. `method.py` runs in about one second; `audit_rederive.py` takes about 10 seconds.

## 4. Expected outputs and where they appear
- `results/grid_values.csv` — all intermediates on the 41-point grid (0–4000 m, 100 m steps).
- `results/summary.json` — test results, structural term s at 1–4 km, max and RMS error, verdicts.
  - Isothermal structural term: s(1000 m) = 0.037 K, s(2000 m) = 0.148 K, s(3000 m) = 0.332 K, s(4000 m) = 0.588 K.
  - Isothermal max |err| = 0.588 K at 4000 m; RMS = 0.269 K; margin to the 0.6 K limit = 0.012 K → borderline, no pass/fail claim.
  - Lapse-rate error is zero by construction (it is the reference).
- `results/method_out.json`, `full_method_out.json`, `mini_method_out.json`, `preview_method_out.json` — predictions in the `exp_gen_sol_out` schema (41 examples in the full file).
- `results/log.txt`, `logs/run.log` — run logs including the seven checks.
- Headline numbers belong in the results section of the paper: the structural term and the isothermal max/RMS error above, with the caveat that there are no field measurements.

## 5. Notes
- `make_variants.py` applies the mini/preview rule to the examples list because the formatter script in the aii-json skill accepts only top-level arrays.
- The audit recomputes the isothermal boiling temperatures with a different routine from `method.py`; see `audit_rederive.py` for its output.
