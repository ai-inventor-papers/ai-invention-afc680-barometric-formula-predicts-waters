# Boiling point vs altitude: reference dataset (gen_art_dataset_1)

## What this is
A sourced, schema-validated table for the claim "a simple barometric formula predicts the boiling point of water at altitude, compared with published measurements."

**Result of the collection step: zero independent measured sites were verified.** The plan asked for at least 25 measured sites, with at least 15 before reporting. Web search did not return a site-level boiling record with station pressure that could be checked against its source. Per the plan, no measured record was padded in from equation-derived values, and the holdout set is empty.

What is delivered instead is the equation-derived side only:

1. A reference grid of boiling temperature at 0 to 4000 m in 100 m steps (41 rows, `evidence_type = equation_derived`, `split = reference`). Source: a barometric-levelling table (deleze.name), transcribed by hand from the fetched page.
2. A formula-versus-table check: U.S. Standard Atmosphere 1976 pressure, then an empirical pressure-to-boiling fit (Snyder, UC Davis / hi-tm.com note). Residuals against the grid: mean -0.004 C, max absolute 0.21 C.

**What this does and does not show.** The grid and the formula come from the same barometric model family, so their agreement is a consistency check on the chain. It is not evidence against measurements. The held-out and measured-site comparison that the hypothesis needs is still open.

## Layout
- `temp/datasets/boiling_point_altitude_full.json`: all 41 rows (JSON array).
- `temp/datasets/boiling_point_altitude_mini.json`: first 5 rows.
- `temp/datasets/boiling_point_altitude_preview.json`: first 5 rows, strings truncated to 200 characters.
- `temp/datasets/boiling_point_altitude.csv`: CSV copy of the full table.
- `temp/datasets/summary.json`: counts, altitude range, holdout rule, residual summary, sources.
- `schema/boiling_point_altitude.schema.json`: JSON Schema (Draft 2020-12). All 41 rows validate.
- `code/build_dataset.py`: stdlib-only builder. Regenerates everything in `temp/datasets/`.
- `data.py` (uv inline script): converts the reference table to the `exp_sel_data_out` layout. Outputs `full_data_out.json` (41 examples, one dataset group `boiling_point_altitude_reference_grid`, one example per row, input = elevation only, output = table boiling temperature), `mini_data_out.json` and `preview_data_out.json` (first 3 examples per dataset; preview truncated to 200 characters). `full_data_out.json` also passes jsonschema against `exp_sel_data_out.json` (0 errors). The skill's validator reported failure without detail on this path, so its result is not relied on.
- `drop_log.json`: candidate sources considered and why they were not used.

## Holdout rule (fixed before collection)
Hold out all measured sites in the Americas above 1000 m. No measured sites were verified, so the holdout set is empty in this release. The reference rows are not split.

## Field conventions not met in this release
- Station pressure: none. No measured site had a verified station pressure.
- Thermometer uncertainty and elevation uncertainty: not applicable to the reference grid.
- Licence: the grid values are extracted numbers with a citation. No table body is redistributed.
- Citation access dates: 2026-11-21.

## How to run
```
python3 code/build_dataset.py
python3 -I -c "import json,jsonschema; s=json.load(open('schema/boiling_point_altitude.schema.json')); [jsonschema.validate(r,s) for r in json.load(open('temp/datasets/boiling_point_altitude_full.json'))]; print('ok')"
```
The validation step needs `jsonschema`.

## Restoring removed files
No heavy files are present in this workspace. Nothing is marked for deletion. To regenerate the outputs, run `python3 code/build_dataset.py`.

## Next steps (not done here)
- Find measured boiling records at named sites with a stated thermometer, and a station pressure from a named source (for example NOAA GHCN-Daily element PRES, checked for its station-versus-sea-level convention). Add them as `evidence_type = measured` rows.
- Check the CRC Handbook and Keenan-Keyes or Hilsenrath values directly. The Hilsenrath source (NBS Circular 564) was identified but not fetched.
