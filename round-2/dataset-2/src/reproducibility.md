# Reproducing the boiling-point dataset artifact

This folder is one artifact of a public GitHub repository. Clone the repository and `cd` into this folder before running anything. All paths below are relative to this folder.

## 1. Get the artifact
```bash
git clone <repository-url> measured-boiling-point-records
cd measured-boiling-point-records/<this-artifact-folder>
```

## 2. System packages, Python, environment
- Ubuntu (any recent LTS). No system packages are required beyond `curl` for the source checks.
- Python 3.12 (the build used 3.12.14). Install with `sudo apt install python3.12` or via `uv python install 3.12`.
- uv (the build used uv 0.6.14): `pip install uv` or the install script from astral.sh.
- No third-party libraries. `data.py` imports only `json` and `pathlib`. No `.venv` was created on the build machine, so there are no pinned versions to install. `pyproject.toml` lists `dependencies = []`.

## 3. Downloads, keys and environment variables
- No API keys or environment variables are needed for `data.py`.
- The source search used these public pages (no login needed): the Forbes 1857 paper full text on archive.org (`transactionsofro21royal`), the UC Davis calibration PDF, the Denver Public Library index card, the NOAA NCEI ISD product pages, and the NBS Circular 564 PDF. These are recorded as citation notes in `search/` and `temp/datasets/candidates.json`. Nothing from them is redistributed in full.
- The 2.1 MB archive.org text copy at `temp/src/vol21.txt` is a scratch download. It is under the 10 MB auto-keep floor, so it stays in the folder. It can be re-downloaded from the archive.org URL listed in `temp/datasets/candidates.json` (entry C1).

## 4. Exact commands, in order
1. Source search (recorded, not re-run automatically): `aii_fast_web_search.py` and `aii_fast_web_fetch.py` from the aii-web-tools skill, 8 broad searches plus follow-up fetches. Outputs are in `search/`.
2. Build the dataset file and its variants:
   ```bash
   uv run data.py
   ```
   This writes `full_data_out.json`, `mini_data_out.json` and `preview_data_out.json` in this folder. It reads `temp/datasets/measured_boiling_point_records_full.json`, which holds 0 measured records.
3. Schema check (run the validator in Python against the schema in the aii-json skill; the skill's own command-line validator rejects paths outside the project directory, so use jsonschema directly):
   ```bash
   uv run --with jsonschema python -c "import json,jsonschema; s=json.load(open('<path-to-aii-json>/schemas/exp_sel_data_out.json')); [jsonschema.validate(json.load(open(f)), s) or print(f,'OK') for f in ['full_data_out.json','mini_data_out.json','preview_data_out.json']]"
   ```
   Replace `<path-to-aii-json>` with the local path to the aii-json skill folder. It is not part of this repository.
- Seeds: none (no randomness). Hardware: none needed (CPU, a few seconds). Runtime: under one second.

## 5. What a reader should get
- `full_data_out.json`: one dataset group, `snyder_altitude_boiling_reference_tierC`, with 4 Tier C reference rows. These are equation-derived values stated in the Snyder table: 212.0 F at 0 ft, 210.2 F at 1,000 ft, 208.4 F at 2,000 ft and 206.6 F at 3,000 ft, converted to degrees C. They are not measurements.
- `mini_data_out.json` and `preview_data_out.json`: the first three examples of that group. The preview truncates strings to 200 characters. Both are identical to the full file here, apart from the truncation.
- `measured_boiling_point_records_full.json` (under `temp/datasets/`): zero Tier A and Tier B rows. The 25-site target and the 8-site held-out set are both not met, and no held-out set is defined.
- `candidates.json` and `drop_log.json` (under `temp/datasets/`): every candidate source, its tier and status, and the reason for each drop.
- No paper figures or numbers come from this artifact. The 0-row Tier A result is the finding.

## Inputs and private files
- No user-uploaded files were used. If a reader supplies a copy of the Forbes 1857 table, it would be entered by hand into `temp/datasets/measured_boiling_point_records_full.json` with citation and elevation uncertainty for each row.

## Restoring removed files
No files were deleted from this folder, so nothing needs restoring.
